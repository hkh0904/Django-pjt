<template>
  <div
    :style="{
      'background-image': 'url(' + backimage + ')',
      'background-attachment': 'fixed',
      'background-size': 'cover',
      'background-position': 'center',
      srcset: backimage,
    }"
  >
    <div class="movie_detail">
      <div class="detail_router">
        <router-link class="link" :to="{ name: 'movie_detail' }"
          >Overview</router-link
        >
        |
        <router-link class="link" :to="{ name: 'movie_detail_videos' }"
          >Videos</router-link
        >
        |
        <router-link class="link" :to="{ name: 'movie_detail_photos' }"
          >Photos</router-link
        >
        |
        <router-link class="link" :to="{ name: 'movie_detail_comment' }"
          >Comments</router-link
        >
      </div>
      <div class="content1">
        <div class="poster">
          <img :src="url" class="image" />
        </div>
        <div class="text-box">
          <div class="head_">
            <h2>{{ moviedata_detail.title }}</h2>
          </div>
          <div class="body_">
            <h5>Story</h5>
            <p style="font-size: 13px">{{ moviedata_detail.overview }}</p>
            <div class="b">
              <div class="b_left">
                <p>Popularity</p>
                <p>Release Date</p>
                <p>Vote Average</p>
              </div>
              <div class="b_right">
                <p>{{ moviedata_detail.popularity }}</p>
                <p>{{ moviedata_detail.release_date }}</p>
                <p>{{ moviedata_detail.vote_average }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="content2">
        <div class="home">
          <h1 style="color: white; text-align: left; padding-left: 5%">CAST</h1>
          <div class="slider3-container">
            <button class="nav-button3 slider3-nav-left" @click="slide3(-1)">
              ◁
            </button>
            <div class="slider3" ref="slider3">
              <div
                class="slide3"
                v-for="(movie, index) in cast"
                :key="index"
                :style="{ transform: `translateX(${index * -20}%)` }"
              >
                <div class="item">
                  <img
                    :src="url_actor + movie.profile_path"
                    :alt="movie.id"
                    class="slide3-img"
                  />
                  <p class="item-text">{{ movie.original_name }}</p>
                </div>
              </div>
            </div>
            <button class="nav-button3 slider3-nav-right" @click="slide3(1)">
              ▷
            </button>
          </div>
        </div>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MovieDetail",
  data() {
    return {
      movie_id: null,
      moviedata_detail: [],
      url: null,
      cast: [],
      accessKey: this.$store.state.accessKey,
      url_actor: "https://image.tmdb.org/t/p/w500",
      currentIndex: 0,
      backimage: null,
    };
  },
  created() {
    this.movie_id = this.$route.params.movie_id;

    axios({
      method: "GET",
      url: `https://api.themoviedb.org/3/movie/${this.movie_id}`,
      params: { language: "ko-KR" },
      headers: {
        accept: "application/json",
        Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q`,
      },
    })
      .then((response) => {
        this.$store.commit("GET_MOVIES_DETAIL", response.data);
        this.moviedata_detail = this.$store.state.movie_detail;
        this.url =
          "https://image.tmdb.org/t/p/w500" + this.moviedata_detail.poster_path;
        // this.backimage =
        //   "https://image.tmdb.org/t/p/w500" +
        //   this.$store.state.movie_detail.belongs_to_collection.backdrop_path;
      })
      .catch(function (error) {
        console.error(error);
      });

    axios({
      method: "GET",
      url: `https://api.themoviedb.org/3/movie/${this.movie_id}/credits?language=ko-KR`,
      headers: {
        accept: "application/json",
        Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q`,
      },
    })
      .then((response) => {
        this.cast = [];
        for (let i = 0; i < response.data.cast.length; i++) {
          if (response.data.cast[i].popularity >= 5) {
            this.cast.push(response.data.cast[i]);
          }
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  },

  methods: {
    slide3(direction) {
      const slider = this.$refs.slider3;
      const slides = slider.querySelectorAll(".slide3");
      const slideWidth = slides[0].offsetWidth; // 슬라이드 한 개의 너비
      const maxIndex = slides.length - 1; // 슬라이드의 마지막 인덱스

      // 인덱스 변경
      this.currentIndex += direction;

      // 범위 검사
      if (this.currentIndex < 0) {
        this.currentIndex = maxIndex;
      } else if (this.currentIndex > maxIndex) {
        this.currentIndex = 0;
      }

      // 슬라이드 이동
      const translateX = -this.currentIndex * slideWidth;
      slider.style.transform = `translateX(${translateX}px)`;
    },
  },
};
</script>

<style scoped>
.movie_detail {
  width: 100%;
  height: 100%;
}

#app {
  background-color: #141414;
}

.home {
  width: 100%;
}

.detail_router {
  width: 90%;
  height: auto;
  line-height: 55px;
  margin-left: 6%;
  text-align: right;
}

.detail_router .link {
  color: white;
  text-decoration: none;
  transition: color 0.2s ease-in-out;
}

.detail_router .link:hover {
  color: #6e6e6e;
}

.content1 {
  width: 90%;
  height: 40%;
  margin-top: 3%;
  margin-left: auto;
  margin-right: auto;
  display: flex;
}

.poster {
  width: 35%;
  height: auto;
}

.image {
  width: 300px;
  height: 450px;
  padding: 5px;
}

.text-box {
  width: 65%;
  height: 100%;
}

.head_ {
  width: auto;
  height: 50%;
  color: white;
  text-align: left;
  padding: 2%;
}

.body_ {
  width: auto;
  height: 50%;
  text-align: left;
  color: white;
  padding: 2%;
}

.b {
  display: flex;
  margin-top: 6%;
}

.b_left {
  margin-right: 7%;
}

.link_ {
  width: auto;
  height: 50%;
  border: 2px solid black;
}

.content2 {
  width: 90%;
  height: 40%;
  margin-top: 5%;
  margin-left: auto;
  margin-right: auto;
}

.nav-button3 {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 3%;
  height: 88%;
  margin-top: -25px;
  background-color: rgba(83, 83, 83, 0.4);
  font-size: 24px;
  line-height: 1100%;
  border-radius: 3px;
  color: #000;
  outline: none;
  border: none;
}

.nav-button3:hover {
  background-color: rgba(0, 0, 0, 0.4);
}

.slider3-container {
  width: 95%;
  margin-left: 5%;
  overflow: hidden;
  display: flex;
  position: relative;
}

.slider3 {
  display: flex;
  height: 100%;
  width: 300px;
  transition: transform 0.3s ease-in-out;
}

.slide3 {
  flex: 0 0 15%;
  padding-right: 8px;
}

.slide3-img {
  width: 200px;
  height: 300px;
  height: 300px;
  object-fit: cover;
  cursor: pointer;
  padding-right: 8px;
  margin-left: 0px;
}

.slider3-nav {
  display: flex;
  margin-top: 10px;
  left: 0;
}

.slider3-nav-left {
  display: flex;
  align-items: left;
  transform: translateY(-50%);
  z-index: 1;
  left: 0;
}

.slider3-nav-right {
  display: flex;
  align-items: right;
  transform: translateY(-50%);
  z-index: 1;
  right: 0;
}
</style>
