<template>
  <div>
    <div class="main-box">
      <div class="poster-box">
        <b-container class="searchBar">
          <b-row>
            <b-col cols="10" style="padding-right: 0">
              <b-input
                v-model="query"
                placeholder="Search"
                @keyup.enter="searchMovie"
              />
            </b-col>
            <b-col cols="2" style="padding-left: 0">
              <b-button @click="searchMovie">Search</b-button>
            </b-col>
          </b-row>
        </b-container>
        <div v-if="searchResult.length != 0">
          <hr />
          <h1 style="color: white">"{{ query }}" 검색결과</h1>
          <br />
        </div>
        <div class="container1">
          <div class="row row-cols-xxl-3 g-10">
            <div
              class="col1 image-container"
              v-for="movie in searchResult"
              :key="movie.id"
            >
              <img
                :src="movieImg(movie.poster_path)"
                style="width: 100%; cursor: pointer"
              />
              <div class="overlay" @click="goDetail(movie.id)">
                <h5 class="fw-bold">{{ movie.title }}</h5>
                <h5>{{ movie.vote_average }}</h5>
              </div>
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
  name: "SearchMovies",
  data() {
    return {
      query: null,
      searchResult: [],
    };
  },
  methods: {
    movieImg(movie_path) {
      return `https://image.tmdb.org/t/p/w500${movie_path}`;
    },
    goDetail(movie_id) {
      return this.$router.push({
        name: "movie_detail",
        params: { movie_id: movie_id },
      });
    },
    searchMovie() {
      const url = "https://api.themoviedb.org/3/search/movie";
      const params = {
        query: this.query,
        include_adult: false,
        language: "ko-KR",
        page: 1,
      };
      const headers = {
        Authorization:
          "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YzBkM2E5ZDA4NTk5N2E5YTIxMTBkMjc5NWJmYjE2NCIsInN1YiI6IjYzZDMxY2FhMDMxYTFkMDA4OTIyNWI0MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.wXalzc_nBAtE4kt4OwXZotadAhvCCRJpiowCbtAQ3Hs",
      };

      axios
        .get(url, { params, headers })
        .then((res) => {
          this.searchResult = res.data.results;
          console.log(this.searchResult);
        })
        .catch((error) => {
          console.error("error:" + error);
        });
    },
  },
};
</script>

<style scoped>
.main-box {
  width: 80%;
  height: auto;
  margin: auto;
  padding-bottom: 40px;
  margin-top: 150px;
}

.container1 {
  height: auto;
  padding-top: 2%;
  overflow: hidden;
}

.col1 {
  width: 25%;
  margin-bottom: 30px;
  padding: 0 8px;
}
.image-container {
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  overflow: hidden;
}

.image-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.searchBar {
  width: 70%;
  margin-bottom: 50px;
}
.image-container {
  position: relative;
  display: inline-block;
  padding: 0px;
  width: 200px;
  height: 300px;
  margin: 10px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s ease;
  padding-top: 60%;
  cursor: pointer;
}

.image-container:hover .overlay {
  opacity: 1;
}
</style>
