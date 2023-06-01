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
    <div class="box">
      <iframe :src="video" width="100%" height="800"></iframe>
      <hr />
      <br />
      <h3 style="color: white; text-align: left">
        Video List &nbsp;&nbsp;<span style="font-size: 20px; color: azure"
          >{{ video_list.length }} videos</span
        >
      </h3>
      <div class="container2">
        <div class="row row-cols-xxl-3 g-10">
          <div class="col2" v-for="(movie, idx) in video_list" :key="idx">
            <iframe :src="movie" width="100%" height="300" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MovieDetailVideo",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      movie_id: null,
      video: null,
      video_list: [],
    };
  },
  created() {
    this.movie_id = this.$route.params.movie_id;

    axios({
      method: "GET",
      url: `https://api.themoviedb.org/3/movie/${this.movie_id}/videos?language=en-US`,
      headers: {
        accept: "application/json",
        Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q`,
      },
    })
      .then((response) => {
        let flag = 0;
        for (let i = 0; i < response.data.results.length; i++) {
          if (flag === 0) {
            this.video_list.push(
              "https://www.youtube.com/embed/" + response.data.results[i].key
            );
            if (response.data.results[i].type === "Trailer") {
              this.video =
                "https://www.youtube.com/embed/" + response.data.results[i].key;
              flag = 1;
            }
          } else {
            this.video_list.push(
              "https://www.youtube.com/embed/" + response.data.results[i].key
            );
          }
        }
      })
      .catch(function (error) {
        console.error(error);
      });
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
.box {
  width: 90%;
  height: auto;
  margin: auto;
  padding-bottom: 20px;
}

.box-list {
  width: 100%;
  height: auto;
  margin: auto;
  border: 2px solid pink;
  padding-bottom: 20px;
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
