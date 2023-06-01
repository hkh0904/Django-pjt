<template>
  <div class="main">
    <div class="main-box">
      <div class="left-box">
        <div class="left-body">
          <div class="left-title">
            <div class="title-left">
              <h2 class="fw-bold" style="margin-left: 15px; margin-top: 70px">
                {{ article.title }}
              </h2>
            </div>
            <div class="title-right">
              <div>
                <button
                  v-if="article.likes.includes(loggedInUser.pk)"
                  @click="likeArticle(article_id)"
                  id="like"
                >
                  💔
                </button>
                <button v-else @click="likeArticle(article_id)" id="like">
                  💖
                </button>
              </div>
              <div>
                <p
                  style="
                    margin-top: -30px;
                    text-align: right;
                    margin-right: 15px;
                  "
                >
                  ♥ {{ article.likes.length }}
                </p>
                <p style="margin-right: 15px">
                  writer :
                  <span
                    @click="goProfile(article.user)"
                    style="cursor: pointer"
                  >{{ article.username }}</span
                  >
                  | Post number :
                  {{ article.id }}
                </p>
              </div>
            </div>
          </div>
          <div class="left-content">
            <h4>
              {{ article.content }}
            </h4>
          </div>
          <div class="left-bottom">
            <div class="left-bottom-left">
              <p style="">Created - {{ article.created_at }}</p>
              <p>Last Update - {{ article.updated_at }}</p>
            </div>
            <div class="left-bottom-right">
              <div class="left-bottom-like">
                <b-button
                  variant="outline-info"
                  @click="backList"
                  style="margin-right: 15px; margin-top: 10px"
                  >back</b-button
                >
              </div>
              <div class="left-bottom-update">
                <b-button
                  v-if="article.user === loggedInUser.pk"
                  variant="outline-warning"
                  @click="updateArticle(article_id, loggedInUser.pk)"
                  >update</b-button
                >
              </div>
              <div class="left-bottom-del">
                <b-button
                  v-if="article.user === loggedInUser.pk"
                  v-b-modal.modal-center
                  variant="outline-danger"
                  >delete</b-button
                >

                <b-modal id="modal-center" size="sm" centered title="Delete">
                  <template>
                    <h5>정말 삭제하시겠습니까?</h5>
                  </template>

                  <template #modal-footer="{ cancel }">
                    <b-button
                      size="sm"
                      variant="danger"
                      @click="deleteArticle()"
                    >
                      Delete
                    </b-button>

                    <b-button
                      size="sm"
                      variant="outline-secondary"
                      @click="cancel()"
                    >
                      Cancel
                    </b-button>
                  </template>
                </b-modal>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="right-box">
        <div class="right-content">
          <CommentsView :article_id="article_id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";

import CommentsView from "@/components/CommentsView.vue";

export default {
  name: "article_detail",
  components: {
    CommentsView,
  },
  data() {
    return {
      loggedInUser: this.$store.state.loggedInUser,
      accessKey: this.$store.state.accessKey,
      article: null,
      article_id: null,
      like_toggle: false,
    };
  },
  async created() {
    this.article_id = this.$route.params.article_id;
    await this.getArticle();
    this.getUserData();
  },
  computed: {
    imagePath() {
      const userId = this.user.profile_img;
      return require(`@/assets/Profile_img0${userId}.png`);
    },
  },
  methods: {
    backList() {
      this.$router.push({ name: "articles" });
    },
    getArticle() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/${this.article_id}`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((response) => {
          this.article = response.data;

          this.article.created_at = response.data.created_at.slice(0, 16);
          this.article.updated_at = response.data.updated_at.slice(0, 16);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteArticle() {
      axios({
        method: "DELETE",
        url: `${API_URL}/articles/${this.article_id}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          this.$router.push({ name: "articles" });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateArticle(article_id) {
      this.$router.push({
        name: "article_update",
        params: { article_id: article_id },
      });
    },
    likeArticle(article_id) {
      axios({
        method: "POST",
        url: `${API_URL}/articles/${article_id}/like/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          if (this.article.likes.includes(this.loggedInUser.pk)) {
            // 이미 좋아요한 경우, 좋아요를 취소합니다.
            const index = this.article.likes.indexOf(this.loggedInUser.pk);
            this.article.likes.splice(index, 1);
          } else {
            // 좋아요하지 않은 경우, 좋아요를 추가합니다.
            this.article.likes.push(this.loggedInUser.pk);
          }
        })
        .catch((error) => {
          console.error(error);
        });
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
.main {
  padding-top: 30px;
  padding-bottom: 30px;
}
.main-box {
  width: 90%;
  border: 2px solid white;
  padding: 30px;
  display: flex;
  background-color: rgb(248, 248, 228);
  border-radius: 15px;
  margin: auto;
  margin-bottom: 30px;
  margin-top: 30px;
}
.left-box {
  width: 60%;
  height: 720px;
  /* border: 2px solid pink; */
  padding: 30px;
}
.left-body {
  width: 100%;
  height: 100%;
  border: 1px solid rgb(221, 220, 220);
  box-shadow: 3px 3px 0 3px rgb(223, 223, 223, 0.5);
  border-radius: 8px;
  padding: 13px;
}

.left-title {
  width: 100%;
  height: 20%;
  /* border: 2px solid orange; */
  display: flex;
  justify-content: space-between;
}

.left-content {
  width: 100%;
  height: 70%;
  /* border: 2px solid orange; */
  text-align: left;
  padding: 15px;
  background-color: white;
  border-radius: 15px;
}
.left-bottom {
  width: 100%;
  height: 10%;
  /* border: 2px solid orange; */
  display: flex;
  justify-content: space-between;
}

.left-bottom-right {
  display: flex;
}

.left-bottom-left {
  text-align: left;
  margin-top: 15px;
  margin-left: 10px;
  line-height: 10px;
}

#like {
  background-color: rgb(248, 248, 228);
  border: none;
  font-size: 25px;
  margin-right: -80px;
  margin-top: 50px;
}

.left-bottom-update {
  margin-right: 15px;
  margin-top: 10px;
}

.left-bottom-del {
  margin-top: 10px;
}

.right-box {
  width: 40%;
  height: 720px;
  /* border: 2px solid pink; */
  padding: 30px;
}
.right-content {
  width: 100%;
  height: 100%;
  /* border: 2px solid orangered; */
}
</style>
