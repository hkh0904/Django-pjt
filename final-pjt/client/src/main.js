import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueKinesis from "vue-kinesis";

import VueYoutube from "vue-youtube";

import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import { VueSpinners } from "@saeris/vue-spinners";

import VueModal from "vue-js-modal";

import VueSwing from "vue-swing";

// Import Bootstrap and BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
Vue.use(VueYoutube);
Vue.use(VueKinesis);
Vue.use(VueSpinners);
Vue.use(VueModal);
Vue.component("vue-swing", VueSwing);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
