<template>
  <div>
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
    <div class="main-box">
      <div class="poster-box">
        <div>
          <h1 style="color: white; text-align: left; margin-left: 30px">
            POSTER
          </h1>
        </div>
        <div class="container1">
          <div class="row row-cols-xxl-3 g-10">
            <div class="col1" v-for="(movie, idx) in poster" :key="idx">
              <img :src="movie" style="width: 100%" />
            </div>
          </div>
        </div>
      </div>
      <hr style="color: aliceblue" />
      <div class="back-box">
        <div>
          <h1 style="color: white; text-align: left; margin-left: 30px">
            BACKDROP
          </h1>
        </div>
        <div class="container2">
          <div class="row row-cols-xxl-3 g-10">
            <div class="col2" v-for="(movie, idx) in background" :key="idx">
              <img :src="movie" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MovieDetailPhotos",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      currentIndex: 0,
      movie_id: null,
      poster: [],
      background: [],
    };
  },
  created() {
    this.movie_id = this.$route.params.movie_id;

    axios({
      method: "GET",
      url: `https://api.themoviedb.org/3/movie/${this.movie_id}/images`,
      headers: {
        accept: "application/json",
        Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q`,
      },
    })
      .then((response) => {
        const tmp = [];
        const tmp_back = [];
        for (let i = 0; i < response.data.posters.length; i++) {
          if (
            response.data.posters[i].vote_average > 5.2 &&
            response.data.posters[i].iso_639_1 === "ko"
          ) {
            tmp.push(
              "https://image.tmdb.org/t/p/w500" +
                response.data.posters[i].file_path
            );
          }
        }

        for (let i = 0; i < response.data.backdrops.length; i++) {
          if (response.data.backdrops[i].vote_average > 5.2) {
            tmp_back.push(
              "https://image.tmdb.org/t/p/w500" +
                response.data.backdrops[i].file_path
            );
          }
        }
        this.poster = tmp;
        this.background = tmp_back;
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
      const translateX = -this.currentIndex * (slideWidth - 80);
      slider.style.transform = `translateX(${translateX}px)`;
    },

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
      const translateX = -this.currentIndex * (slideWidth - 100);
      slider.style.transform = `translateX(${translateX}px)`;
    },
  },
};
</script>

<style scoped>
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
.main-box {
  width: 90%;
  height: auto;
  margin: auto;
  padding-bottom: 40px;
  /* display: flex; */
}

.poster-box {
  width: 100%;
  height: auto;
  position: relative;
  overflow: hidden;
  align-items: left;
}

.container1 {
  height: auto;
  display: flex;
  margin-left: 0px;
  padding-top: 2%;
}

.col1 {
  margin-left: 3%;
  margin-bottom: 30px;
  width: 30%;
}

.back-box {
  width: 100%;
  height: auto;
  position: relative;
  overflow: hidden;
}

.container2 {
  height: auto;
  display: flex;
  padding-top: 2%;
}

.col2 {
  margin-bottom: 30px;
}
</style>
