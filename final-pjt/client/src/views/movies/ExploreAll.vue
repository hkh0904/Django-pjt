<template>
  <div>
    <div class="main-box">
      <div class="poster-box">
        <div>
          <br />
          <h1 style="color: white; text-align: left; margin-left: 0%">
            POSTER <span style="font-size: 25px">/ {{ name }}</span>
          </h1>
          <hr />
        </div>
        <div class="container1">
          <div class="row row-cols-xxl-3 g-10">
            <div
              class="col1 image-container"
              v-for="movie in movies"
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
export default {
  name: "ExploreAll",
  data() {
    return {
      movie_data: [],
      movies: [],
      name: null,
    };
  },
  created() {
    this.name = this.$route.params.name;

    if (this.name === "Recent Movies") {
      this.movie_data = this.$store.state.movies;
      for (let i = 0; i < this.movie_data.length; i++) {
        this.movies.push(this.movie_data[i]);
      }
    } else if (this.name === "Upcomming Movies") {
      this.movie_data = this.$store.state.upcomming_movies;
      for (let i = 0; i < this.movie_data.length; i++) {
        this.movies.push(this.movie_data[i]);
      }
    } else if (this.name === "HarryPotter Series") {
      this.movie_data = this.$store.state.harry;
      for (let i = 0; i < this.movie_data.length; i++) {
        this.movies.push(this.movie_data[i]);
      }
    }
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
  },
};
</script>

<style scoped>
.main-box {
  width: 90%;
  height: auto;
  margin: auto;
  padding-bottom: 40px;
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
