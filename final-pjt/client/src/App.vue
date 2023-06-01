<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <router-link :to="{ name: 'main' }"
        ><img
          src="./assets/GoonManDu.png"
          style="width: 20%; margin-left: -80px"
      /></router-link>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav style="justify-content: flex-end">
        <b-navbar-nav style="align-items: center">
          <b-nav-form>
            <router-link
              :to="{ name: 'searchMovie' }"
              style="font-size: 25px; cursor: pointer"
              >🔎</router-link
            >
          </b-nav-form>
          <b-nav-item style="margin-left: 10px">
            <router-link :to="{ name: 'home' }" style="margin-right: 10px"
              >Home</router-link
            >
          </b-nav-item>
          <b-nav-item>
            <router-link
              :to="{ name: 'recommended' }"
              style="margin-right: 10px"
              >Rec</router-link
            >
          </b-nav-item>
          <b-nav-item>
            <router-link
              :to="{ name: 'articles' }"
              style="margin-right: 10px"
              @click="reload"
              >Com</router-link
            >
          </b-nav-item>

          <!-- 로그인 모달 -->
          <b-nav-item v-if="!isLogin">
            <span
              class="fw-bold login-txt"
              style="margin-bottom: 0px; color: #2c3e50"
              v-b-modal.modal-center
            >
              LogIn
            </span></b-nav-item
          >
          <b-modal id="modal-center" hide-header>
            <div class="d-block text-center">
              <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
              <p class="text-50 mb-5">Please enter your ID and Password!</p>
            </div>
            <div class="form-outline mb-4">
              <label class="form-label fw-bold" for="input-username">ID</label>
              <b-form-input
                id="input-username"
                placeholder="ID"
                v-model="username"
                :state="nameState"
                aria-describedby="input-live-feedback"
                trim
              ></b-form-input>

              <b-form-invalid-feedback
                id="input-username-feedback"
                class="text-right"
              >
                알파벳/숫자 3글자 이상
              </b-form-invalid-feedback>
            </div>

            <div class="form-outline mb-4">
              <label class="form-label fw-bold" for="input-password"
                >Password</label
              >
              <b-form-input
                id="input-password"
                placeholder="PASSWORD"
                v-model="password"
                :state="passwordState"
                aria-describedby="input-username-feedback"
                trim
                type="password"
                autocomplete="false"
                @keyup.enter="login"
              ></b-form-input>

              <b-form-invalid-feedback
                id="input-password-feedback"
                class="text-right"
              >
                비밀번호 8글자 이상
              </b-form-invalid-feedback>
            </div>
            <b-container>
              <b-row>
                <b-button variant="primary" @click="login"> Login </b-button>
              </b-row>
            </b-container>
            <template #modal-footer="{ cancel }">
              <!-- Emulate built in modal footer ok and cancel button actions -->
              <b-button variant="secondary" @click="cancel()">
                Cancel
              </b-button>
            </template>
          </b-modal>

          <b-nav-item v-if="!isLogin">
            <router-link
              :to="{ name: 'signup' }"
              style="padding-left: 0; margin-right: 10px"
              >SignUp</router-link
            >
          </b-nav-item>
          <b-nav-item v-if="isLogin">
            <router-link :to="{ name: 'myprofile' }" style="margin-right: 10px"
              >My</router-link
            >
          </b-nav-item>
          <b-nav-item v-if="isLogin">
            <span
              class="fw-bold login-txt"
              style="margin-bottom: 0px; color: #2c3e50; margin-right: 10px"
              @click="logout"
              type="submit"
            >
              LogOut
            </span>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view />
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";
export default {
  name: "app",
  data() {
    return {
      loggedInUser: this.$store.state.loggedInUser.pk,
      username: "",
      password: "",
      query: "",
    };
  },
  computed: {
    nameState() {
      if (!this.username) {
        return;
      }
      return this.username.length >= 3 ? true : false;
    },
    passwordState() {
      if (!this.password) {
        return;
      }
      return this.password.length >= 8 ? true : false;
    },
    isLogin() {
      return this.$store.getters.isLogin;
    },
  },
  methods: {
    reload() {
      this.$router.push({ name: "recommended" });
      location.reload();
    },
    logout() {
      this.$store.commit("LOGOUT");
    },
    login() {
      const username = this.username;
      const password = this.password;

      axios({
        method: "POST",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          this.$store.commit("SAVE_ACCESS", res.data);
          const isLoggedIn = this.$store.getters.isLogin;
          if (isLoggedIn) {
            this.$bvModal.hide("modal-center");
          }
        })
        .catch((err) => {
          console.log(err);
          alert("아이디와 비밀번호를 확인해주세요!");
        });
      this.username = "";
      this.password = "";
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Signika+Negative:wght@300;500&display=swap");
#app {
  font-family: "Nanum Gothic", sans-serif;
  font-family: "Signika Negative", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
  text-decoration: none !important;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none !important;
}

nav a:hover {
  color: aquamarine;
}

nav a.router-link-exact-active {
  color: #ffffff;
  /* #4DB1E2s -> 아이폰 파란색 컬러 */
}
.navbar {
  display: flex;
  align-items: center;
}

.b-navbar-nav .nav-link {
  text-decoration: none !important;
}

.login-txt:hover {
  color: aquamarine;
}

.login-txt:active {
  color: white;
}

.col {
  margin: 0px;
}

.b-navbar-nav .nav-link .fw-bold.login-txt {
  color: aquamarine;
}

.b-navbar-nav .nav-link.router-link-exact-active {
  color: #ffffff;
}
</style>
