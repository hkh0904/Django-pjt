<template>
  <section class="background-radial-gradient overflow-hidden">
    <div class="container px-4 py-5 px-md-5 text-center text-lg-start my-5">
      <div class="row gx-lg-5 align-items-center mb-5">
        <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10">
          <h1
            class="my-5 display-5 fw-bold ls-tight"
            style="color: hsl(218, 81%, 95%)"
          >
            Thank you <br />
            <span style="color: hsl(218, 81%, 75%)"
              >for registering as a member</span
            >
          </h1>
          <p class="mb-4 opacity-70" style="color: hsl(218, 81%, 85%)">
            Our site is a movie recommendation site, and we recommend movies
            that suit users' tastes with a large amount of movie data. It also
            provides a variety of information, including the latest movies,
            movie rankings, and series.
          </p>
        </div>

        <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
          <div
            id="radius-shape-1"
            class="position-absolute rounded-circle shadow-5-strong"
          ></div>
          <div
            id="radius-shape-2"
            class="position-absolute shadow-5-strong"
          ></div>

          <div class="card bg-glass">
            <div class="card-body px-4 py-5 px-md-5">
              <form>
                <!-- username input -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="input-username"
                    >Username</label
                  >
                  <b-form-input
                    id="input-username"
                    v-model="username"
                    :state="nameState"
                    aria-describedby="input-live-feedback"
                    trim
                  ></b-form-input>
                  <b-form-invalid-feedback
                    id="input-username-feedback"
                    class="text-end"
                  >
                    알파벳/숫자 3글자 이상
                  </b-form-invalid-feedback>
                </div>

                <!-- Email input -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="input-email">Email</label>
                  <b-form-input
                    id="input-email"
                    v-model="email"
                    :state="emailState"
                    aria-describedby="input-live-feedback"
                    trim
                  ></b-form-input>
                  <b-form-invalid-feedback
                    id="input-email-feedback"
                    class="text-end"
                  >
                    E-Mail 형식입력
                  </b-form-invalid-feedback>
                </div>

                <!-- Password input -->
                <div class="form-outline mb-4">
                  <label class="form-label" for="input-password1"
                    >Password</label
                  >
                  <b-form-input
                    type="password"
                    id="input-password1"
                    class="form-control"
                    v-model="password1"
                    :state="password1State"
                    aria-describedby="input-password1-feedback"
                    trim
                    autocomplete="false"
                  ></b-form-input>
                  <b-form-invalid-feedback
                    id="input-password1-feedback"
                    class="text-end"
                    >비밀번호 8글자 이상
                  </b-form-invalid-feedback>
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" for="input-password2"
                    >Password check</label
                  >
                  <b-form-input
                    type="password"
                    id="input-password2"
                    class="form-contro2"
                    v-model="password2"
                    :state="password2State"
                    aria-describedby="input-password2-feedback"
                    trim
                    autocomplete="false"
                    @keyup.enter="signup"
                  ></b-form-input>
                  <b-form-invalid-feedback
                    id="input-password2-feedback"
                    class="text-end"
                    >비밀번호 불일치
                  </b-form-invalid-feedback>
                </div>
                <!-- Submit button -->
                <div class="text-center">
                  <button
                    type="button"
                    class="btn btn-secondary btn-lg btn-block mb-4"
                    @click="signup"
                  >
                    Sign up
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      password2: "",
    };
  },
  computed: {
    nameState() {
      if (this.username.length === 0) {
        return;
      }
      return this.username.length >= 3 ? true : false;
    },
    emailState() {
      if (this.email.length === 0) {
        return;
      }
      return this.email.indexOf("@") !== -1 ? true : false;
    },
    password1State() {
      if (this.password1.length === 0) {
        return;
      }
      return this.password1.length >= 8 ? true : false;
    },
    password2State() {
      if (this.password2.length === 0) {
        return;
      }
      return this.password2.length >= 8 && this.password1 === this.password2
        ? true
        : false;
    },
  },
  methods: {
    signup() {
      const username = this.username;
      const email = this.email;
      const password1 = this.password1;
      const password2 = this.password2;

      if (
        username.length === 0 ||
        email.length === 0 ||
        password1.length === 0 ||
        password2.length === 0
      ) {
        alert("빠진 정보 없이 입력해주세요");
        return;
      }

      const payload = {
        username,
        email,
        password1,
        password2,
      };
      this.$store.dispatch("signup", payload);
    },
  },
};
</script>

<style>
.login-form {
  border-radius: 20px;
  background-color: rgb(220, 242, 248);
  box-shadow: 20px 20px 10px 0px lightgray;
}

.background-radial-gradient {
  background-color: hsl(218, 41%, 15%);
  background-image: radial-gradient(
      650px circle at 0% 0%,
      hsl(221, 10%, 49%) 15%,
      hsl(218, 12%, 40%) 35%,
      hsl(219, 15%, 25%) 75%,
      hsl(217, 17%, 15%) 80%,
      transparent 100%
    ),
    radial-gradient(
      1250px circle at 100% 100%,
      hsl(221, 10%, 49%) 15%,
      hsl(218, 12%, 40%) 35%,
      hsl(219, 15%, 25%) 75%,
      hsl(217, 17%, 15%) 80%,
      transparent 100%
    );
}

#radius-shape-1 {
  height: 220px;
  width: 220px;
  top: -60px;
  left: -130px;
  background: radial-gradient(#2b2a2c, #827d85);
  overflow: hidden;
}

#radius-shape-2 {
  border-radius: 38% 62% 63% 37% / 70% 33% 67% 30%;
  bottom: -60px;
  right: -110px;
  width: 300px;
  height: 300px;
  background: radial-gradient(#2b2a2c, #827d85);
  overflow: hidden;
}

.bg-glass {
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  backdrop-filter: saturate(200%) blur(25px);
}
</style>
