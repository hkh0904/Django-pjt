<template>
  <div class="back">
    <div class="main-box">
      <div class="content-box">
        <div
          style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-right: 15px;
          "
        >
          <div>
            <h1 style="text-align: left; margin-left: 20px; margin: 20px">
              Articles
            </h1>
          </div>
          <div>
            <button
              v-if="isLogin"
              @click="showModal"
              style="
                border-radius: 25px;
                font-size: 30px;
                width: 50px;
                height: 50px;
                border: #fff0a6 1px solid;
                background-color: #fff0a6;
              "
            >
              +
            </button>
            <b-modal v-model="modalOpen" title="Create Article">
              <p>Title</p>
              <b-input
                type="text"
                v-model="title"
                maxlength="20"
                aria-placeholder="20자 미만으로 적어주세요"
              />
              <p>Content</p>
              <div class="textarea-wrapper">
                <b-textarea
                  type="text"
                  v-model="content"
                  rows="10"
                  :max-rows="10"
                  no-resize
                  class="form-control"
                />
              </div>

              <template #modal-footer>
                <div class="d-flex justify-content-end">
                  <b-button @click="createArticle" variant="success"
                    >작성</b-button
                  >
                  <b-button @click="closeModal" variant="danger">취소</b-button>
                </div>
              </template>
            </b-modal>
          </div>
        </div>
        <div class="list-container">
          <ul>
            <div
              class="list"
              v-for="article in visibleArticles"
              :key="article.id"
            >
              <div
                class="list-title fw-bold"
                style="cursor: pointer"
                @click="article_click(article.id)"
              >
                <p style="margin-bottom: 0px">
                  {{ article.id }}.&nbsp;
                  <span>
                    {{ article.title }}
                  </span>
                </p>
              </div>
              <div class="list-icon">
                <span class="list-title" @click="goProfile(article.user)" style="cursor: pointer">
                  <img
                    :src="getUserProfileImage(article.user)"
                    style="height: 20px"
                  />
                  {{ article.username }}
                </span>
                <span>🧡 {{ article.likes.length }} </span>
                <span> 💬 {{ getCommentCount(article.id) }}</span>
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
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";

export default {
  name: "articleList",
  data: function () {
    return {
      articles: [],
      isLogin: this.$store.getters.isLogin,
      accessKey: this.$store.state.accessKey,
      comments: [],
      replys: [],
      page: 1,
      pageSize: 5,
      userProfileImages: [],
      user: this.$store.state.loggedInUser,
      title: null,
      content: null,
      modalOpen: false, // 모달 열림/닫힘 상태
    };
  },
  created() {
    if (!this.$store.state.accessKey) {
      alert("커뮤니티는 로그인 후 이용하실 수 있습니다.");
      this.$router.push({ name: "signup" });
    }
    this.getArticles();
    this.getComments();
    this.getReplys();
  },
  computed: {
    getCommentCount() {
      return (articleId) => {
        const comments = this.comments.filter(
          (comment) => comment.article === articleId
        );
        const replys = this.replys.filter((reply) =>
          comments.some((comment) => comment.id === reply.comment)
        );
        return comments.length + replys.length;
      };
    },
    visibleArticles() {
      const startIndex = (this.page - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.articles.slice(startIndex, endIndex);
    },
    hasNextPage() {
      return this.page * this.pageSize < this.articles.length;
    },
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
    getArticles() {
      axios({
        method: "get",
        url: `${API_URL}/articles/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.articles = res.data;
          for (const article of this.articles) {
            const userId = article.user; // 게시글 작성자 아이디
            this.getImagePath(userId);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getComments() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/comments/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.comments = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getReplys() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/replys/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.replys = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deletearticle: function (article) {
      axios({
        method: "delete",
        url: `${API_URL}/articles/${article.id}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          this.getArticles();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    createArticle() {
      this.$router.push({ name: "createArticle" });
    },
    article_click(article_id) {
      this.$router.push({
        name: "article_detail",
        params: { article_id: article_id },
      });
    },
    nextPage() {
      if (this.hasNextPage) {
        this.page++;
      }
    },
    previousPage() {
      if (this.page > 1) {
        this.page--;
      }
    },
    createArticle() {
      const user = this.user.pk;
      const username = this.user.username;
      const title = this.title;
      const content = this.content;
      if (!title) {
        alert("할 일을 입력해주세요");
        return;
      }
      console.log(user, username, title, content);
      axios({
        method: "post",
        url: `${API_URL}/articles/`,
        data: { user, username, title, content },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          this.getArticles(); // 새로운 글 목록 가져오기
          this.closeModal(); // 모달 닫기
        })
        .catch((err) => {
          console.log(err);
        });
    },
    showModal() {
      // 모달 열기
      this.modalOpen = true;
    },
    closeModal() {
      // 모달 닫기
      this.modalOpen = false;
    },
    goProfile(userId) {
      return this.$router.push({
        name: "profile",
        params: { account_id: userId },
      });
    },
  },
};
</script>

<style scoped>
.article-btn {
  margin-left: 10px;
}

.back {
  padding-bottom: 85px;
  padding-top: 85px;
}
.main-box {
  width: 90%;
  height: 720px;
  /* border: 2px solid white; */
  margin: 0px auto 0px auto;
  padding: 20px;
}

.content-box {
  width: 100%;
  height: 100%;
  /* border: 2px solid snow; */
  background-color: rgb(248, 248, 228);
  border-radius: 15px;
  padding: 15px;
}

.list {
  margin-left: -15px;
  width: 100%;
  border: rgb(228, 228, 227) 1px solid;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  align-items: center;
  margin-bottom: 30px;
}

.list-container {
  height: 500px;
  max-height: 500px; /* Set the maximum height of the list container */
  overflow-y: auto; /* Enable vertical scroll if content exceeds max height */
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-left: 0px;
  position: relative;
}

.pagination-button {
  text-decoration: none !important;
  border-bottom: none !important;
  height: 100%;
}
.pagination {
  text-align: center;
}
.pagination b-button {
  margin-right: 10px;
}
.page-number {
  margin: 0 10px;
  font-weight: bold;
}

.textarea-wrapper {
  display: inline-block;
  width: 100%;
}

.textarea-wrapper .form-control {
  height: auto;
  min-height: 100px; /* 원하는 높이로 조정 */
  resize: vertical;
}

.list-title:hover {
  color: cornflowerblue;
}
</style>
