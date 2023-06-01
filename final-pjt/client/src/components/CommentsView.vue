<template>
  <div class="main">
    <div class="re-title"><h3 style="margin-top: 40px">Comments</h3></div>
    <div class="re-list">
      <ul
        v-for="comment in comments"
        :key="comment.id"
        style="margin-left: -30px"
      >
        <div class="re-one">
          <div style="font-size: large">📌 {{ comment.content }}</div>
          <div style="font-size: medium; color: gray">
            <div>
              <span class="goProfile" @click="goProfile(comment.user)">{{ comment.username }}</span>
              <button v-if="user.id === comment.user" @click="deleteComment(comment.id)" class="icon">
                ❌
              </button>
              <button @click="toggleReplyInput(comment)" class="icon">
                💬
              </button>
            </div>
          </div>
        </div>
        <div class="re_">
          <ReplysView
            :comment_id="comment.id"
            :show_replyInput="comment.show_reply"
            @reply-created="updateShowReplyInput(comment)"
          />
        </div>
      </ul>
    </div>
    <div class="re-input">
      <b-input
        v-model="new_comment"
        @keyup.enter="createComment"
        class="input-box"
      ></b-input>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";

import ReplysView from "./ReplysView.vue";
export default {
  name: "CommentsView",
  components: {
    ReplysView,
  },
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      userId: this.$store.state.loggedInUser.pk,
      user: [],
      comments: [],
      new_comment: null,
      show_replyInput: false,
    };
  },
  props: {
    article_id: {
      type: String,
      required: true,
    },
  },
  created() {
    this.getUserData();
    this.getComments();
  },
  methods: {
    toggleReplyInput(comment) {
      comment.show_reply = !comment.show_reply;
    },
    updateShowReplyInput(comment) {
      comment.show_reply = false;
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
    getComments() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/comments/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.comments = [];
          for (let i = 0; i < res.data.length; i++) {
            if (res.data[i].article == this.article_id) {
              this.comments.push(res.data[i]);
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    createComment() {
      const article = this.article_id;
      const content = this.new_comment;
      const user = this.user.id;
      const username = this.user.username
      console.log(this.user)
      axios({
        method: "post",
        url: `${API_URL}/articles/${article}/comments/`,
        data: { user, username, content },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((response) => {
          const id = response.data.id;
          this.comments.push({ id, user, username, article, content});
          this.new_comment = null;
          this.getComments();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteComment(commentId) {
      axios({
        method: "delete",
        url: `${API_URL}/articles/comments/${commentId}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
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
    goProfile(userId) {
      return this.$router.push({
        name: "profile",
        params: { account_id: userId },
      });
    }
  },
};
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
  /* border: 2px solid black; */
  padding: 15px;
}

.re-title {
  width: 100%;
  height: 100px;
  /* border: 2px solid black; */
  text-align: left;
}
.re-list {
  width: 100%;
  max-height: 466px;
  /* border: 2px solid black; */
  margin-top: -40px;
  padding: 15px;
  overflow-y: scroll;
}

.re-one {
  width: 100%;
  height: auto;
  background-color: white;
  border-radius: 8px;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  padding: 5px;
}

.re-input {
  width: 100%;
  height: auto;
  /* border: 2px solid black; */
}

.icon {
  border: none;
  background-color: white;
}

.input-box:focus {
  outline: none !important;
  border-color: #fdf186;
  box-shadow: 0 0 10px #e9e5a8;
}

.re_ {
  display: flex;
  justify-content: flex-end;
}

.goProfile {
  color: lightslategrey;
  cursor: pointer;
}
.goProfile:hover {
  color: deepskyblue
}
</style>
