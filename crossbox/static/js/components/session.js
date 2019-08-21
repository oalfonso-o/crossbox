
Vue.use(Buefy.default)

Vue.component('session', {
  props: {
    prop_reservations: Array,
    prop_reservated: Boolean,
    session: Number,
    session_closed: Boolean,
    url_reservation_delete: RegExp,
    url_reservation_create: RegExp,
    url_get_is_too_late: RegExp,
    page: Number,
    date: String,
  },
  template: `
    <div v-if="session !== undefined">
      <script type="text/x-template" id="modal-template">
        <transition name="modal">
          <div class="modal-mask">
            <div class="modal-wrapper">
              <div class="modal-container">

                <div class="modal-header">
                  <slot name="header">default header</slot>
                </div>

                <div class="modal-body">
                  <slot name="body">default body</slot>
                </div>

                <div class="modal-footer">
                  <button class="modal-default-button" @click="$emit('confirm')">
                    <slot name="confirm_text">
                      Confirmar
                    </slot>
                  </button>
                  <button class="modal-default-button" @click="$emit('close')">
                    Cancelar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </script>
      <modal v-if="showModal" @close="showModal = false" @confirm="reservated = !reservated; showModal = false">
        <h3 slot="header" v-if="reservated">Vas a anular:</h3>
        <h3 slot="header" v-if="!reservated">Vas a reservar:</h3>
        <h3 slot="body">{{ date }}</h3>
        <span slot="confirm_text" v-if="reservated">
          Anular reserva
        </span>
        <span slot="confirm_text" v-if="!reservated">
          Reservar
        </span>
      </modal>

      <div v-if="reservations.length < 5" class="num_reservations num_reservations_low">
        {{ reservations.length }} / 15
      </div>
      <div v-else-if="reservations.length >= 5 && reservations.length < 15" class="num_reservations num_reservations_open">
        {{ reservations.length }} / 15
      </div>
      <div v-else class="num_reservations num_reservations_closed">
        {{ reservations.length }} / 15
      </div>
      <div class="outer_toggle">
        <div class="inner_toggle">
          <b-checkbox v-model="reservated" type="is-success" :disabled="checkbox_disabled" @click.native="confirm($event)"></b-checkbox>
        </div>
      </div>
      <b-notification auto-close :active.sync="notification_active">
        {{ notification_text }}
      </b-notification>
      <div v-on:click="show_reservation = !show_reservation" class="session_component">
        <div class="show_hide_people">
          <span v-if="show_reservation">Ocultar asistentes</span>
          <span v-else>Mostrar asistentes</span>
        </div>
        <div v-if="show_reservation && reservations.length" class="people_list">
          <li v-for="r in reservations" class="people_li">
            {{ r }}
          </li>
        </div>
      </div>
    </div>
  `,
  data: function () {
    return {
      show_reservation: false,
      reservated: this.prop_reservated,
      reservations: this.prop_reservations,
      notification_active: false,
      notification_text: '',
      is_too_late: false,
      showModal: false,
    }
  },
  created: function() {
    if (this.session) {
      axios.post(this.url_get_is_too_late, { session: this.session })
        .then(response => {
          this.is_too_late = response.data.is_too_late
        }).catch(error => {
          console.log(error.response.data.result)
        })
    }
  },
  watch: {
    reservated: function (value) {
      this.toggle(value)
    },
  },
  computed: {
    form_url: function () {
      return this.reservated ? this.url_reservation_create : this.url_reservation_delete
    },
    checkbox_disabled: function () {
      return (
        (!this.reservated && this.reservations.length == 15)
        || this.session_closed
        || (this.is_too_late && this.reservated && this.reservations.length >= 5)
      )
    }
  },
  methods:{
    confirm: function (event) {
      event.preventDefault()
      this.showModal = true
    },
    toggle: function (value) {
      if (!this.checkbox_disabled) {
        axios.post(this.form_url, { session: this.session, page: this.page })
        .then(response => {
          username_index = this.reservations.indexOf(response.data.username)
          if (response.data.result == 'created') {
            this.reservations.push(response.data.username)
            document.getElementById("wods").textContent = response.data.wods;
            if (response.data.wods == 1) {
              this.notification_text = 'Solo te queda 1 wod'
              this.notification_active = true
            }
          } else if (response.data.result == 'deleted' && username_index != -1) {
            this.reservations.splice(username_index, 1)
            document.getElementById("wods").textContent = response.data.wods;
          }
        }).catch(error => {
          if (error.response.data.result == 'no_wods') {
            this.reservated = false
            this.notification_text = 'No quedan Wods'
            this.notification_active = true
          } else if (error.response.data.result == 'is_too_late') {
            this.reservated = true
            this.is_too_late = true
            this.notification_text = 'Ya no se puede anular'
            this.notification_active = true
          }
        })
      }
    },
  }
})
