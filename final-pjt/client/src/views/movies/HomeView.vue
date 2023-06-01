<template>
  <div class="bb">
    <!-- <img :src="mainurl" class="img" /> -->
    <div class="img-wrapper">
      <div
        class="video-wrapper"
        style="
          width: 100%;
          height: 0;
          margin-top: -100px;
          padding-bottom: 60%;
          position: relative;
        "
      >
        <youtube
          :video-id="videoId"
          :player-vars="playerVars"
          width="100%"
          height="100%"
          style="
            position: absolute;
            top: -100px;
            left: 0;
            width: 100%;
            height: 100%;
          "
          ref="player"
          @ended="ended"
        ></youtube>
      </div>
      <div class="overlay_bot">
        <p class="text" style="font-size: 15px">
          {{ maindata_detail.title }}
        </p>
        <!-- <p class="text" style="font-size: 15px">
          vote_average : {{ maindata_detail.vote_average }}
        </p> -->
        <!-- <p class="text" style="font-size: 17px">줄거리</p> -->
        <br />
        <p class="text" style="font-size: 12px">
          {{ maindata_detail.overview }}
        </p>
        <br />
        <p v-if="maindata_detail.homepage">{{ maindata_detail.homepage }}</p>
        <p class="text" style="font-size: 12px" v-else></p>
        <div style="display: flex">
          <p
            class="text"
            style="font-size: 12px"
            v-for="(item, idx) in maindata_detail.genres"
            :key="idx"
          >
            | {{ item.name }} |
          </p>
        </div>
      </div>
    </div>

    <div class="home">
      <h2 style="color: white; text-align: left; margin-left: 5%">
        Recent Movies
        <span
          class="explore-text"
          @click="exploreall_('Recent Movies')"
          > / Explore All</span
        >
      </h2>

      <div class="slider1-container">
        <button class="nav-button1 slider1-nav-left" @click="slide1(-1)">
          ◁
        </button>
        <div class="slider1" ref="slider1">
          <div
            class="slide1"
            v-for="(movie, index) in recent_movies"
            :key="index"
            :style="{ transform: `translateX(${index * -20}%)` }"
          >
            <div class="item">
              <div class="image-container">
                <img
                  :src="url + movie.poster_path"
                  :alt="movie.title"
                  class="slide1-img"
                  @click="image_click(movie.id)"
                />
              </div>
              <p class="item-text">{{ movie.title }}</p>
              <div>
                <star-rating
                  :border-width="4"
                  border-color="#d8d8d8"
                  :rounded-corners="true"
                  :star-points="[
                    23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34,
                    46, 19, 31, 17,
                  ]"
                  :rating="recent_movies_star[index]"
                  :read-only="true"
                  :star-size="15"
                  :increment="0.1"
                ></star-rating>
              </div>
            </div>
          </div>
        </div>
        <button class="nav-button1 slider1-nav-right" @click="slide1(1)">
          ▷
        </button>
      </div>
    </div>

    <div class="home">
      <h2 style="color: white; text-align: left; margin-left: 5%">
        Upcomming Movies
        <span
        class="explore-text"
          @click="exploreall_('Upcomming Movies')"
          > / Explore All</span
        >
      </h2>
      <div class="slider2-container">
        <button class="nav-button2 slider2-nav-left" @click="slide2(-1)">
          ◁
        </button>
        <div class="slider2" ref="slider2">
          <div
            class="slide2"
            v-for="(movie, index) in upcomming_movies"
            :key="index"
            :style="{ transform: `translateX(${index * -20}%)` }"
          >
            <div class="item">
              <div class="image-container">
                <img
                  :src="url + movie.poster_path"
                  :alt="movie.title"
                  class="slide2-img"
                  @click="image_click(movie.id)"
                />
              </div>
              <p class="item-text">{{ movie.title }}</p>
              <div>
                <star-rating
                  :border-width="4"
                  border-color="#d8d8d8"
                  :rounded-corners="true"
                  :star-points="[
                    23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34,
                    46, 19, 31, 17,
                  ]"
                  :rating="upcomming_movies_star[index]"
                  :read-only="true"
                  :star-size="15"
                  :increment="0.1"
                ></star-rating>
              </div>
            </div>
          </div>
        </div>
        <button class="nav-button2 slider2-nav-right" @click="slide2(1)">
          ▷
        </button>
      </div>
    </div>

    <div class="home">
      <h2 style="color: white; text-align: left; margin-left: 5%">
        Series - Harry Potter
        <span
        class="explore-text"
          @click="exploreall_('HarryPotter Series')"
          >/ Explore All</span
        >
      </h2>
      <div class="slider3-container">
        <button class="nav-button3 slider3-nav-left" @click="slide3(-1)">
          ◁
        </button>
        <div class="slider3" ref="slider3">
          <div
            class="slide3"
            v-for="(movie, index) in harry"
            :key="index"
            :style="{ transform: `translateX(${index * -20}%)` }"
          >
            <div class="item">
              <div class="image-container">
                <img
                  :src="url + movie.poster_path"
                  :alt="movie.title"
                  class="slide3-img"
                  @click="image_click(movie.id)"
                />
              </div>

              <p class="item-text">{{ movie.title }}</p>
              <star-rating
                :border-width="4"
                border-color="#d8d8d8"
                :rounded-corners="true"
                :star-points="[
                  23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34,
                  46, 19, 31, 17,
                ]"
                :rating="harry_star[index]"
                :read-only="true"
                :star-size="15"
                :increment="0.1"
              ></star-rating>
            </div>
          </div>
        </div>
        <button class="nav-button3 slider3-nav-right" @click="slide3(1)">
          ▷
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import StarRating from "vue-star-rating";

export default {
  name: "HomeView",
  data() {
    return {
      mainurl: "https://image.tmdb.org/t/p/w500",
      url: "https://image.tmdb.org/t/p/w500",
      accessKey: this.$store.state.accessKey,
      maindata_detail: [],
      recent_movies: [],
      recent_movies_star: [],
      upcomming_movies: [],
      upcomming_movies_star: [],
      currentIndex: 0, // 현재 보여지는 슬라이드의 인덱스
      harry: [],
      harry_star: [],

      videourl: "https://www.googleapis.com/youtube/v3/search",
      videoId: "RjNcTBXTk4I",
      playerVars: {
        autoplay: 1,
        loop: 1,
        mute: 1,
      },
    };
  },

  components: {
    StarRating,
  },
  created() {
    this.getMovies();
    this.img();
  },
  methods: {
    getMovies() {
      // 최신 영화
      this.$store.dispatch("getMovies");
      this.recent_movies = this.$store.state.movies;

      const tmp_star = [];
      for (let i = 0; i < this.recent_movies.length; i++) {
        tmp_star.push(
          Number((Number(this.recent_movies[i].vote_average) / 2).toFixed(1))
        );
      }
      this.recent_movies_star = tmp_star;
      // 상영 예정작
      this.$store.dispatch("getUpcommingMovies");
      this.upcomming_movies = this.$store.state.upcomming_movies;

      const tmp_star2 = [];
      for (let i = 0; i < this.upcomming_movies.length; i++) {
        tmp_star2.push(
          Number((Number(this.upcomming_movies[i].vote_average) / 2).toFixed(1))
        );
      }
      this.upcomming_movies_star = tmp_star2;

      // 해리포터
      this.$store.dispatch("getHarry");
      const data = this.$store.state.harry;
      const tmp = [];
      const release = [];

      //해리포터 데이터 정렬
      for (let i = 0; i < data.length; i++) {
        tmp.push(Number(data[i].release_date.slice(0, 4)));
      }
      tmp.sort();

      for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < tmp.length; j++) {
          if (Number(data[j].release_date.slice(0, 4)) === tmp[i]) {
            release.push(data[j]);
          }
        }
      }
      this.harry = release;

      const tmp_star3 = [];
      for (let i = 0; i < this.harry.length; i++) {
        tmp_star3.push(
          Number((Number(this.harry[i].vote_average) / 2).toFixed(1))
        );
      }
      this.harry_star = tmp_star3;
    },
    img() {
      this.$store.state.movies[0].postrer_path;
      this.mainurl += this.$store.state.movies[0].backdrop_path;
      const id = this.$store.state.movies[0].id;
      const accessKey = this.accessKey;
      axios({
        method: "GET",
        url: `https://api.themoviedb.org/3/movie/${id}?language=ko-KR`,
        headers: {
          accept: "application/json",
          Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q`,
        },
      })
        .then((response) => {
          this.$store.commit("GET_MOVIES_DETAIL", response.data);
          this.maindata_detail = this.$store.state.movie_detail;
        })
        .catch(function (error) {
          console.log(accessKey);
          console.error(error);
        });
    },

    // 슬라이드 최신 영화
    slide1(direction) {
      const slider = this.$refs.slider1;
      const slides = slider.querySelectorAll(".slide1");
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

    // 슬라이드 상영 예정작
    slide2(direction) {
      const slider = this.$refs.slider2;
      const slides = slider.querySelectorAll(".slide2");
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

    // 슬라이드 g해리포터
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

    image_click(movie_id) {
      return this.$router.push({
        name: "movie_detail",
        params: {
          movie_id: movie_id,
        },
      });
    },
    exploreall_(name) {
      this.$router.push({
        name: "exploreall",
        params: {
          name: name,
        },
      });
    },
    ended() {
      this.$refs.player.player.seekTo(0);
    },
  },
};
</script>

<style scope>
.bb {
  background-color: #141414;
}

#app {
  background-color: #141414;
}

.home {
  width: 95%;
  /* border: 2px solid black; */
  margin: auto;
  margin-top: 5%;
}

.item-text {
  color: white;
  font-size: small;
  text-align: left;
  margin-right: 10%;
  margin-top: 4%;
}

.img-wrapper {
  position: relative;
  width: 100%;
  height: 60vh;
  margin: auto;
  overflow: hidden;
}

.img {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: auto;
  z-index: 2;
  transition: opacity 0.3s ease-out;
}

.img:hover {
  opacity: 0.4;
}

/* .overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 1);
  z-index: 1;
  transform: translateX(-100%);
  transition: transform 0.3s ease-out;
} */

.img:hover ~ .overlay {
  transform: translateX(0);
}

.overlay_bot {
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 5px;
  position: absolute;
  bottom: 0;
  left: 2%;
  width: 30%;
}
.text {
  color: #ffffff;
  margin: 0;
  text-align: left;
}

/* 슬라이드1 */
.nav-button1 {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2%;
  height: 78%;
  margin-top: -42px;
  background-color: rgba(83, 83, 83, 0.4);
  font-size: 24px;
  line-height: 1100%;
  border-radius: 3px;
  color: #000;
  outline: none;
  border: none;
}

.item {
  margin-right: 35px;
}
.nav-button1:hover {
  background-color: rgba(0, 0, 0, 0.4);
}

.slider1-container {
  width: 90%;
  margin-left: 5%;
  overflow: hidden;
  display: flex;
  position: relative;
}

.slider1 {
  display: flex;
  height: 100%;
  width: 300px;
  transition: transform 0.3s ease-in-out;
}

.slide1 {
  flex: 0 0 20%;
  margin-right: 8px;
}

.slide1-img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  cursor: pointer;
  padding-right: 10px;
  margin-left: 0px;
}

.slide1-img:hover {
  box-shadow: 0 16px 16px rgba(255, 255, 255, 0.4); /* Apply the shadow effect on hover */
}

.slider1-nav {
  display: flex;
  margin-top: 10px;
  left: 0;
}

.slider1-nav-left {
  display: flex;
  align-items: left;
  transform: translateY(-50%);
  z-index: 1;
  left: 0;
}

.slider1-nav-right {
  display: flex;
  align-items: right;
  transform: translateY(-50%);
  z-index: 1;
  right: 0;
}

/* 슬라이드2 */
.nav-button2 {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2%;
  height: 78%;
  margin-top: -42px;
  background-color: rgba(83, 83, 83, 0.4);
  font-size: 24px;
  line-height: 1100%;
  border-radius: 3px;
  color: #000;
  outline: none;
  border: none;
}

.nav-button2:hover {
  background-color: rgba(0, 0, 0, 0.4);
}

.slider2-container {
  width: 90%;
  margin-left: 5%;
  overflow: hidden;
  display: flex;
  position: relative;
}

.slider2 {
  display: flex;
  height: 100%;
  width: 300px;
  transition: transform 0.3s ease-in-out;
}

.slide2 {
  flex: 0 0 20%;
  margin-right: 8px;
}

.slide2-img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  cursor: pointer;
  padding-right: 10px;
  margin-left: 0px;
}

.slide2-img:hover {
  box-shadow: 0 16px 16px rgba(255, 255, 255, 0.4); /* Apply the shadow effect on hover */
}

.slider2-nav {
  display: flex;
  margin-top: 10px;
  left: 0;
}

.slider2-nav-left {
  display: flex;
  align-items: left;
  transform: translateY(-50%);
  z-index: 1;
  left: 0;
}

.slider2-nav-right {
  display: flex;
  align-items: right;
  transform: translateY(-50%);
  z-index: 1;
  right: 0;
}

/* 슬라이드3 */
.nav-button3 {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2%;
  height: 80%;
  margin-top: -30px;
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
  width: 90%;
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
  flex: 0 0 20%;
  margin-right: 8px;
}

.slide3-img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  cursor: pointer;
  padding-right: 10px;
  margin-left: 0px;
}

.slide3-img:hover {
  box-shadow: 0 16px 16px rgba(255, 255, 255, 0.4); /* Apply the shadow effect on hover */
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
.explore-text {
  font-size: 18px;
  cursor: pointer;
}
.explore-text:hover {
  color: aquamarine
}
</style>
