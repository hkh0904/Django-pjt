<template>
  <div class="re-box">
    <ul v-for="reply in replys" :key="reply.id" style="margin-left: -30px">
      <div class="list">
        <div class="left">
          <p>🗨 {{ reply.content }}</p>
        </div>
        <div class="right">
          <span style="color: lightslategrey">{{ reply.username }}</span>
          <button v-if="user.id === reply.user" @click="deletereply(reply.id)" class="icon">🗑</button>
        </div>
      </div>
    </ul>
    <b-input
      v-if="show_replyInput"
      v-model="new_reply"
      @keyup.enter="createreply"
      id="input-box"
    ></b-input>
    <br />
  </div>
</template>

//
<script>
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";

export default {
  name: "ReplysView",
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      userId: this.$store.state.loggedInUser.pk,
      user: [],
      replys: [],
      new_reply: null,
    };
  },
  props: {
    comment_id: {
      type: Number,
      required: true,
    },
    show_replyInput: {
      type: Boolean,
      required: true,
    },
  },
  created() {
    this.getUserData();
    this.getreplys();
  },
  methods: {
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
    getreplys() {
      axios({
        method: "GET",
        url: `${API_URL}/articles/replys/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          for (let i = 0; i < res.data.length; i++) {
            if (res.data[i].comment == this.comment_id) {
              this.replys.push(res.data[i]);
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    createreply() {
      const comment = this.comment_id;
      const content = this.new_reply;
      const user = this.user.id;
      const username = this.user.username
      axios({
        method: "post",
        url: `${API_URL}/articles/${comment}/replys/`,
        data: { user, username, content },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((response) => {
          const id = response.data.id;
          this.new_reply = null;
          this.replys.push({ id, user, username, comment, content });
          this.$emit("reply-created");
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deletereply(replyId) {
      axios({
        method: "delete",
        url: `${API_URL}/articles/replys/${replyId}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          for (let i = 0; i < this.replys.length; i++) {
            if (this.replys[i].id === replyId) {
              this.replys.splice(i, 1);
              return;
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
//
</script>

<style>
.main {
  width: 100%;
  align-content: right;
}
.icon {
  border: none;
  background-color: rgb(248, 248, 228);
}

.re-box {
  width: 90%;
  align-items: right;
  margin-bottom: -30px;
}
.list {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: right;
}

#input-box:focus {
  outline: none !important;
  border-color: #fdf186;
  box-shadow: 0 0 10px #e9e5a8;
  margin-top: 10px;
}
</style>
