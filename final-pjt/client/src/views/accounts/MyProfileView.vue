<template>
  <div style="padding: 50px">
    <div class="main-box">
      <div class="left-box">
        <div class="left-image">
          <div style="margin-top: 30px">
            <img
              alt="ProfileImg"
              :src="getImagePath(user.profile_img)"
              style="width: 200px"
            />
            <faDriversLicense>
              <h1 style="margin-top: 30px; color: snow">MyProfile</h1>
            </faDriversLicense>
            <span style="color: snow"
              >팔로잉 : {{ followers.length }} | 팔로워
              {{ user.followings.length }}</span
            >
          </div>
        </div>

        <div class="left-user">
          <div style="text-align: left">
            <h4>› My Id</h4>
            <br />
            <h4>› UserName</h4>
            <br />
            <h4>› E-mail</h4>
          </div>
          <div style="text-align: left; margin-left: 20%">
            <h4>{{ user.username }}</h4>
            <br />
            <h4>{{ user.nickname }}</h4>
            <br />
            <h4>{{ user.email }}</h4>
          </div>
        </div>
        <div style="margin-top: 20px; margin-left: 40%">
          <b-button
            @click="modalShow = !modalShow"
            style="margin-right: 25px; color: snow"
            variant="outline-dark"
            >Change PW</b-button
          >
          <b-button
            @click="updateUser"
            style="color: snow"
            variant="outline-dark"
            >회원 정보 수정</b-button
          >
        </div>
      </div>
      <b-modal v-model="modalShow" id="modal-scoped">
        <template #modal-header>
          <h5 class="fw-bold">Password Change</h5>
        </template>

        <template #default>
          <p class="fw-bold">New Password</p>
          <b-input type="password" v-model="new_pw1"></b-input><br />
          <p class="fw-bold">New Password Check</p>
          <b-input
            type="password"
            v-model="new_pw2"
            @keyup.enter="changePW"
          ></b-input
          ><br />
        </template>

        <template #modal-footer="{ cancel }">
          <b-button size="sm" variant="success" @click="changePW">
            Change
          </b-button>
          <b-button size="sm" variant="danger" @click="cancel()">
            Cancel
          </b-button>
        </template>
      </b-modal>
      <div class="right-box">
        <div class="r-l">
          <h2 class="fw-bold" style="text-align: left; color: snow">
            My Articles
          </h2>
          <div style="height: 77%">
            <div v-for="article in displayArticles" :key="article.id">
              <div class="text article-box">
                <router-link
                  :to="{
                    name: 'article_detail',
                    params: { article_id: article.id },
                  }"
                  style="text-decoration: none; color: black"
                  >✔ {{ article.title }}</router-link
                >
              </div>
            </div>
          </div>

          <div class="pagination">
            <span
              @click="previousPage"
              :disabled="currentPage === 1"
              style="cursor: pointer"
            >
              ◁ &nbsp;&nbsp;
            </span>
            <span>{{ currentPage }}&nbsp;&nbsp;</span>
            <span
              @click="nextPage"
              :disabled="currentPage === totalPages"
              style="cursor: pointer"
            >
              ▷
            </span>
          </div>
        </div>

        <div class="r-r">
          <h2 class="fw-bold" style="text-align: left; color: snow">
            My Comments
          </h2>
          <div style="height: 77%">
            <div v-for="comment in displayArticles2" :key="comment.id">
              <div class="text comment-box">
                <router-link
                  :to="{
                    name: 'movie_detail',
                    params: { movie_id: comment.movie },
                  }"
                  style="text-decoration: none; color: black"
                  >✔ {{ comment.content }} |
                  {{ comment.moviename }}</router-link
                >
              </div>
            </div>
          </div>
          <div class="pagination2">
            <span
              @click="previousPage2"
              :disabled="currentPage2 === 1"
              style="cursor: pointer"
            >
              ◁ &nbsp;&nbsp;
            </span>
            <span>{{ currentPage2 }}&nbsp;&nbsp;</span>
            <span
              @click="nextPage2"
              :disabled="currentPage2 === totalPages2"
              style="cursor: pointer"
            >
              ▷
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";
export default {
  name: "MyProfile",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      loggedInUser: this.$store.state.loggedInUser.pk,
      user: [],
      articles: [],
      followers: [],
      comments: [],
      modalShow: false,
      new_pw1: null,
      new_pw2: null,

      // articles: [], // 모든 게시물 데이터 배열
      perPage: 5, // 한 페이지에 표시될 항목 수
      currentPage: 1, // 현재 페이지

      // articles2: [], // 모든 게시물 데이터 배열
      perPage2: 5, // 한 페이지에 표시될 항목 수
      currentPage2: 1, // 현재 페이지
    };
  },
  created() {
    this.getUserData();
    this.getFollowers();
    this.getArticles();
    this.getComments();
  },
  computed: {
    isFollowing() {
      return this.followers.some(
        (follower) => follower.id === this.loggedInUser
      );
    },

    totalPages() {
      return Math.ceil(this.articles.length / this.perPage); // 전체 페이지 수 계산
    },
    displayArticles() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.articles.slice(startIndex, endIndex); // 현재 페이지에 해당하는 게시물만 추출
    },

    totalPages2() {
      return Math.ceil(this.comments.length / this.perPage2); // 전체 페이지 수 계산
    },
    displayArticles2() {
      const startIndex2 = (this.currentPage2 - 1) * this.perPage2;
      const endIndex2 = startIndex2 + this.perPage2;
      return this.comments.slice(startIndex2, endIndex2); // 현재 페이지에 해당하는 게시물만 추출
    },
  },
  methods: {
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
            if (this.loggedInUser == res.data[i].user) {
              this.comments.push(res.data[i]);
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    changePW() {
      const new_password1 = this.new_pw1;
      const new_password2 = this.new_pw2;
      axios({
        method: "POST",
        url: `${API_URL}/accounts/password/change/`,
        data: { new_password1, new_password2 },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          alert("비밀번호가 변경되었습니다.");
          this.modalShow = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getImagePath(userImg) {
      return require(`@/assets/Profile_img0${userImg}.png`);
    },
    getUserData() {
      axios({
        method: "get",
        url: `${API_URL}/account/userinfo/${this.loggedInUser}/`,
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
    getFollowers() {
      axios({
        method: "GET",
        url: `${API_URL}/account/follow/${this.loggedInUser}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.followers = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getArticles() {
      axios({
        method: "get",
        url: `${API_URL}/articles/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          for (let i = 0; i < res.data.length; i++) {
            if (this.loggedInUser === res.data[i].user) {
              this.articles.push(res.data[i]);
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateUser() {
      this.$router.push({ name: "userUpdate" });
    },
    follow() {
      axios({
        method: "POST",
        url: `${API_URL}/account/follow/${this.loggedInUser}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.followers = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    previousPage2() {
      if (this.currentPage2 > 1) {
        this.currentPage2--;
      }
    },
    nextPage2() {
      if (this.currentPage2 < this.totalPages2) {
        this.currentPage2++;
      }
    },
  },
};
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  color: white;
}

.pagination button {
  margin: 0 0.5rem;
}
.pagination2 {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  color: white;
}

.pagination2 button {
  margin: 0 0.5rem;
}
.main-box {
  width: 90%;
  height: 800px;
  /* border: 2px solid white; */
  margin: auto;
  display: flex;
  justify-content: center;
  align-content: center;
  text-align: center;
}

.left-box {
  width: 40%;
  /* border: 2px solid pink; */
  /* margin-left: auto; */
  margin-right: 100px;
  margin-left: -100px;
}

.right-box {
  width: 30%;
  /* border: 2px solid pink; */
  /* background-color: snow; */
  border-radius: 15px;
}

.left-image {
  width: 100%;
  height: 350px;
  margin-top: 100px;
  /* border: 2px solid orange; */
}
.left-user {
  width: 80%;
  margin: auto;
  height: 230px;
  color: rgb(202, 202, 202);
  border: 2px solid rgb(228, 223, 223);
  border-radius: 20px;
  /* background-color: rgb(228, 223, 223); */
  padding: 35px;
  display: flex;
}
.r-l {
  width: 100%;
  height: 50%;
  /* border: 2px solid orchid; */
  padding: 20px;
}

.article-box {
  width: 100%;
  background-color: snow;
  margin-top: 25px;
  height: 85%;
  border-radius: 15px;
  padding: 15px;
}
.r-r {
  width: 100%;
  height: 50%;
  /* border: 2px solid orchid; */
  padding: 20px;
}
.comment-box {
  width: 100%;
  background-color: snow;
  margin-top: 25px;
  height: 85%;
  border-radius: 15px;
  padding: 15px;
}

.text {
  width: 100%;
  /* background-color: #141414; */
  padding: 5px;
  border-radius: 8px;
}
</style>
