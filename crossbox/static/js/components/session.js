
Vue.use(Buefy.default)

Vue.component('session', {
  props: {
    prop_reservations: Array,
    prop_reservated: Boolean,
    prop_is_too_late: String,
    session: Number,
    session_closed: Boolean,
    url_reservation_delete: RegExp,
    url_reservation_create: RegExp,
    page: Number,
    date: Boolean,
    hour: String,
    user_is_staff: Boolean,
    prop_type: String,
  },
  template: `
    <div>
      <div v-if="session !== undefined" class="row_center_container">
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
                    <b-button class="modal-button modal-close" @click="$emit('close')">Cancelar</b-button>
                    <b-button class="modal-button modal-confirm" @click="$emit('confirm')">
                      <slot name="confirm_text">
                        Confirmar
                      </slot>
                    </b-button>
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
        <div class="session_hour">{{ hour }}</div>

        <div class="session_type">{{ type }}<span v-if=user_is_staff @click="change_session_type()">&nbsp;<i class="fa fa-pencil"></i></span></div>

        <div class="session_checkbox">
          <div class="inner_toggle">
            <b-checkbox v-model="reservated" type="is-success" :disabled="checkbox_disabled" @click.native="confirm($event)"></b-checkbox>
          </div>
        </div>

        <div v-on:click="show_reservation = !show_reservation" class="session_people_list">
          <div class="show_hide_people">
            <span v-if="show_reservation"><i class="fa fa-eye-slash eye-closed"></i></span>
            <span v-else><i class="fa fa-eye"></i></span>
          </div>
          <div v-if="show_reservation && reservations.length" class="people_list">
            <li v-for="reservation in reservations" class="people_li">
              {{ reservation }}
            </li>
          </div>
        </div>

        <div class="session_num_reservations">
          <div v-if="reservations.length < 4" class="num_reservations num_reservations_low">
            {{ reservations.length }} / 12
          </div>
          <div v-else-if="reservations.length >= 4 && reservations.length < 12" class="num_reservations num_reservations_open">
            {{ reservations.length }} / 12
          </div>
          <div v-else class="num_reservations num_reservations_closed">
            {{ reservations.length }} / 12
          </div>
        </div>

        <b-notification auto-close :active.sync="notification_active">
          {{ notification_text }}
        </b-notification>
      </div>
      <div v-if="!session">
        {{ hour }}
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
      is_too_late: this.prop_is_too_late,
      showModal: false,
      type: this.prop_type,
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
        (!this.reservated && this.reservations.length == 12 && !this.prop_reservated)
        || this.session_closed
        || (this.is_too_late && this.reservated && this.reservations.length >= 4 && this.prop_reservated)
      )
    }
  },
  methods:{
    change_session_type: function() {
      axios.put('../change_session_type/' + this.session + '/')
      .then(response => {
        this.type = response.data.session_type
      }).catch(error => {
        if (error.response.data.result == 'session_not_found') {
          this.notification_text = 'Ha habído un error, esa sesión ya no existe.'
          this.notification_active = true
        }
      })
    },
    confirm: function (event) {
      event.preventDefault()
      if (!this.checkbox_disabled) {
        this.showModal = true
      }
    },
    toggle: function (value) {
      if (!this.checkbox_disabled) {
        axios.post(this.form_url, { session: this.session, page: this.page })
        .then(response => {
          username_index = this.reservations.indexOf(response.data.username)
          if (response.data.result == 'created') {
            this.prop_reservated = true
            this.reservations.push(response.data.username)
            document.getElementById("wods").textContent = response.data.wods;
            this.notification_text = 'Reserva realizada!'
            this.notification_active = true
            if (response.data.wods == 1) {
              this.notification_text = 'Solo te queda 1 wod'
              this.notification_active = true
            }
          } else if (response.data.result == 'deleted' && username_index != -1) {
            this.prop_reservated = false
            this.reservations.splice(username_index, 1)
            document.getElementById("wods").textContent = response.data.wods;
            this.notification_text = 'Reserva anulada!'
            this.notification_active = true
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
