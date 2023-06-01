import Vue from "vue";
import Vuex from "vuex";
import router from "../router";
import axios from "axios";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);
const API_URL = "http://127.0.0.1:8000/GoonManDu";

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    accessKey: null,
    loggedInUser: null,
    movies: [],
    movie_detail: [],
    upcomming_movies: [],
    harry: [],
    rec_genres: null,
  },
  getters: {
    isLogin(state) {
      return state.accessKey ? true : false;
    },
  },
  mutations: {
    SAVE_ACCESS(state, data) {
      state.accessKey = data.access;
      state.loggedInUser = data.user;
      if (router.currentRoute.path === "/signup") {
        router.push({ name: "home" });
      } else {
        location.reload();
      }
    },
    LOGOUT(state) {
      alert("로그아웃 되었습니다.");
      state.accessKey = null;
      state.loggedInUser = null;
      state.rec_genres = null;
      if (router.currentRoute.path !== "/home") {
        router.push({ name: "home" });
      } else {
        location.reload();
      }
    },
    GET_MOVIES(state, data) {
      state.movies = data;
    },
    GET_MOVIES_DETAIL(state, data) {
      state.movie_detail = data;
    },
    GET_UPCOMMING_MOVIES(state, data) {
      state.upcomming_movies = data;
    },
    GET_HARRY(state, data) {
      const tmp = [];
      for (let i = 0; i < 8; i++) {
        tmp.push(data[i]);
      }
      state.harry = tmp;
    },
    REC_GENRES(state, data) {
      state.rec_genres = data;
      console.log(state.rec_genres);
    },
  },
  actions: {
    signup(context, payload) {
      const username = payload.username;
      const email = payload.email;
      const password1 = payload.password1;
      const password2 = payload.password2;

      axios({
        method: "POST",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          email,
          password1,
          password2,
        },
      })
        .then((res) => {
          context.commit("SAVE_ACCESS", res.data);
        })
        .catch((err) => {
          const response = JSON.parse(err.request.response);
          const errorMessages = [];

          // 모든 속성을 반복하여 에러 메시지를 배열에 저장
          for (const key in response) {
            if (Array.isArray(response[key])) {
              errorMessages.push(response[key][0]);
            }
          }

          // 배열의 모든 에러 메시지를 결합하여 출력
          const errorMessage = errorMessages.join("\n");
          alert(errorMessage);
        });
    },

    getMovies(context) {
      axios({
        method: "GET",
        url: "https://api.themoviedb.org/3/movie/now_playing",
        params: { language: "ko-KR", page: "1" },
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${context.accessKey}`,
        },
      })
        .then(function (response) {
          context.commit("GET_MOVIES", response.data.results);
        })
        .catch(function (error) {
          console.error(error);
        });
    },

    getMoviesDetail(context, data) {
      axios({
        method: "GET",
        url: `https://api.themoviedb.org/3/movie/${data}`,
        params: { language: "ko-KR" },
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${context.accessKey}`,
        },
      })
        .then(function (response) {
          context.commit("GET_MOVIES_DETAIL", response.data);
        })
        .catch(function (error) {
          console.error(error);
        });
    },

    getUpcommingMovies(context) {
      axios({
        method: "GET",
        url: "https://api.themoviedb.org/3/movie/upcoming",
        params: { language: "ko-KR", page: "1" },
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${context.accessKey}`,
        },
      })
        .then(function (response) {
          context.commit("GET_UPCOMMING_MOVIES", response.data.results);
        })
        .catch(function (error) {
          console.error(error);
        });
    },

    getHarry(context) {
      axios({
        method: "GET",
        url: "https://api.themoviedb.org/3/search/movie",
        params: {
          query: "Harry Potter",
          include_adult: "false",
          language: "ko-KR",
          page: "1",
        },
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${context.accessKey}`,
        },
      })
        .then(function (response) {
          context.commit("GET_HARRY", response.data.results);
        })
        .catch(function (error) {
          console.error(error);
        });
    },
  },
  modules: {},
});
