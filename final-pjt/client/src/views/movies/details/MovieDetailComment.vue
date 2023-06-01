<template>
  <div class="main-box">
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
    <Loading></Loading>
    <div class="content-box">
      <div class="left-box">
        <div class="comment_list">
          <h1 class="text" style="margin-bottom: 20px; margin-left: 30px">
            Comment List
          </h1>
          <div style="height: 470px">
            <ul v-for="(comment, idx) in visibleComments" :key="idx">
              <div class="comment">
                <div class="max" @click="showFullComment(comment)">
                  <star-rating
                    :border-width="4"
                    border-color="#d8d8d8"
                    :rounded-corners="true"
                    :star-points="[
                      23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36,
                      34, 46, 19, 31, 17,
                    ]"
                    :rating="comment.star"
                    :read-only="true"
                    :star-size="15"
                    :increment="0.1"
                  ></star-rating>
                  <p
                    class="text"
                    style="
                      font-size: small;
                      margin-top: 7px;
                      margin-left: 5px;
                      overflow: hidden;
                      text-overflow: ellipsis;
                      white-space: nowrap;
                    "
                  >
                    {{ comment.content }}
                  </p>
                </div>
                <div>
                  <div>
                    <span @click="goProfile(comment.user)">
                      <img
                    :src="getUserProfileImage(comment.user)"
                    style="height: 20px"
                  />
                      {{ comment.username }}</span
                    >
                    <span
                      v-if="user.id === comment.user"
                      @click="deleteComment(comment.id)"
                      style="z-index: 99999"
                      >❌</span
                    >
                  </div>
                </div>
              </div>
              <div v-if="showModal" class="modal">
                <div class="modal-content">
                  <span class="close" @click="showModal = false">&times;</span>
                  <p>{{ selectedComment.content }}</p>
                </div>
              </div>
            </ul>
          </div>
          <div class="pagination-container">
            <div class="pagination">
              <b-button
                variant="link"
                @click="previousPage"
                :disabled="page === 1"
                class="pagination-button"
              >
                ◁
              </b-button>
              <span class="page-number" style="line-height: 35px">{{
                page
              }}</span>
              <b-button
                variant="link"
                @click="nextPage"
                :disabled="!hasNextPage"
                class="pagination-button"
              >
                ▷
              </b-button>
            </div>
          </div>
        </div>
      </div>
      <div class="right-box">
        <div style="margin-bottom: 25px; margin-top: 20px">
          <star-rating
            :animate="true"
            :active-color="['	#FFE000', '	#FFE000']"
            :active-border-color="['#d8d8d8', '#d8d8d8']"
            :border-width="4"
            :star-points="[
              23, 2, 14, 17, 0, 19, 10, 34, 7, 50, 23, 43, 38, 50, 36, 34, 46,
              19, 31, 17,
            ]"
            :active-on-click="true"
            :clearable="true"
            :star-size="38"
            :increment="0.5"
            @rating-selected="setRating"
            v-model="rating"
          ></star-rating>
        </div>
        <p class="text">content</p>
        <b-form-textarea
          id="textarea"
          placeholder="Enter something..."
          rows="14"
          max-rows="20"
          v-model="new_comment"
          @keyup.enter="createComment"
          class="input-box"
        >
        </b-form-textarea>
        <br />
        <div class="create">
          <b-button variant="outline-warning" @click="createComment"
            >Create</b-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "vue-star-rating";

import Loading from "../../../components/Loading.vue";

const API_URL = "http://127.0.0.1:8000/GoonManDu";

export default {
  name: "movieComment",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      movie_id: null,
      comments: [],
      new_star: 0,
      new_comment: null,
      url: null,
      moviedata_detail: [],
      page: 1,
      pageSize: 6,
      star: [],
      rating: null,
      userId: this.$store.state.loggedInUser.pk,
      user: [],
      showModal: false,
      selectedComment: null,
      userProfileImages: [],
    };
  },
  components: {
    StarRating,
    Loading,
  },
  computed: {
    visibleComments() {
      const startIndex = (this.page - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.comments.slice(startIndex, endIndex);
    },
    hasNextPage() {
      return this.page * this.pageSize < this.comments.length;
    },
  },
  created() {
    if (!this.$store.state.accessKey) {
      alert("커뮤니티는 로그인 후 이용하실 수 있습니다.");
      this.$router.push({ name: "signup" });
    }

    this.movie_id = this.$route.params.movie_id;
    this.getComments();
    this.getUserData();
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
      })
      .catch(function (error) {
        console.error(error);
      });
  },
  methods: {
    getUserProfileImage(userId) {
      const userProfile = this.userProfileImages.find(
        (profile) => profile.userId === userId
      );
      return userProfile ? userProfile.imagePath : null;
    },
    getImagePath(userId) {
      axios({
        method: "get",
        url: `${API_URL}/account/userinfo/${userId}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          const imagePath = require(`@/assets/Profile_img0${res.data.profile_img}.png`);
          this.userProfileImages.push({ userId, imagePath });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    goProfile(userId) {
      return this.$router.push({
        name: "profile",
        params: { account_id: userId },
      });
    },
    getComments() {
      axios({
        method: "GET",
        url: `${API_URL}/comments/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          for (let i = 0; i < res.data.length; i++) {
            if (this.movie_id == res.data[i].movie) {
              this.comments.push(res.data[i])
            }
          }
          console.log(this.comments)
          for (const comment of res.data) {
            const userId = comment.user; // 게시글 작성자 아이디
            this.getImagePath(userId);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUserData() {
      axios({
        method: "get",
        url: `${API_URL}/account/userinfo/${this.userId}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.user = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    createComment() {
      const user = this.user.id;
      const username = this.user.username;
      const movie = this.movie_id;
      const moviename = this.moviedata_detail.title
      const content = this.new_comment;
      const star = this.new_star;
      axios({
        method: "post",
        url: `${API_URL}/movies/${movie}/comments/`,
        data: { user, username, movie, moviename, content, star },
      })
        .then((response) => {
          const id = response.data.id;
          this.new_comment = null;
          this.new_star = 0;
          this.comments.push({ id, user, username, movie, moviename, content, star });
        })
        .catch((error) => {
          console.error(error);
        });
      this.rating = 0;
    },
    deleteComment(commentId) {
      axios({
        method: "delete",
        url: `${API_URL}/comments/${commentId}/`,
      })
        .then(() => {
          this.showModal = false; // Add this line to hide the modal
          for (let i = 0; i < this.comments.length; i++) {
            if (this.comments[i].id === commentId) {
              this.comments.splice(i, 1);
              return;
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    nextPage() {
      this.page++;
    },
    previousPage() {
      this.page--;
    },
    setRating: function (rating) {
      this.new_star = rating;
    },
    showFullComment(comment) {
      this.selectedComment = comment;
      this.showModal = true;
    },
  },
};
</script>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 80px;
  margin-left: 0px;
  position: relative;
}

.pagination-button {
  text-decoration: none !important;
  border-bottom: none !important;
  height: 100%;
}
.pagination {
  margin-top: 15px;
  text-align: center;
}
.pagination b-button {
  margin-right: 10px;
}
.page-number {
  margin: 0 10px;
  font-weight: bold;
}

.text {
  color: rgb(0, 0, 0);
}
.detail_router {
  width: 94%;
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
  /* border: 2px solid white; */
  margin: auto;
  padding-bottom: 80px;
}

.content-box {
  width: 100%;
  height: 720px;
  /* border: 2px solid rgb(240, 247, 184); */
  display: flex;
  background-color: rgb(248, 248, 228);
  border-radius: 15px;
  margin-top: 30px;
}
.left-box {
  width: 65%;
  /* border: 2px solid pink; */
  margin: 5px;
  max-width: 60%;
}

.poster-box {
  width: 50%;
}

.detail-box {
  width: 100%;
  padding-top: 85px;
  margin: 1px 1px 1px 1px;
}
.movie-poster {
  width: 100%;
  height: 100%;
  align-items: left;
}
.comment_list {
  max-width: 100%;
  /* border: 2px solid wheat; */
  margin-left: -10px;
  padding: 15px;
  overflow-y: auto;
  text-overflow: ellipsis;
}

.comment {
  display: flex;
  margin-top: 15px;
  border-radius: 10px;
  background-color: white;
  justify-content: space-between;
  padding: 13px;
  max-width: 100%;
  cursor: pointer;
}
.right-box {
  width: 40%;
  border: 1px solid rgb(221, 220, 220);
  box-shadow: 3px 3px 0 3px rgb(223, 223, 223, 0.5);
  padding: 20px;
  border-radius: 8px;
  height: 80%;
  margin-top: 60px;
  margin-left: 0px;
  margin-right: 20px;
}

.create {
  width: 100%;
  text-align: right;
}

.input-box:focus {
  outline: none !important;
  border-color: #fdf186;
  box-shadow: 0 0 10px #e9e5a8;
}

.max {
  height: 52px;
  width: 80%;
}

.modal {
  display: block;
  position: fixed;
  z-index: 99;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  animation: none;
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  max-height: 80%;
  overflow-y: auto;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}


</style>
