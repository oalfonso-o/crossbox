
Vue.component('wods', {
    props: {
      prop_wods: Number,
    },
    template: `
      <div>
        Wods: <span id="wods">{{ wods }}</span>
      </div>`,
    data: function () {
      return {
        wods: this.prop_wods,
      }
    }
  })