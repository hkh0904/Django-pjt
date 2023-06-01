<template>
  <div style="padding: 50px">
    <div class="main-box">
      <div class="left-image">
        <div style="margin-top: 45px">
          <img
            alt="ProfileImg"
            :src="getImagePath(change_Img)"
            style="width: 200px; margin-top: 20px"
          />
        </div>
        <div style="margin-top: 30px">
          <button
            @click="modalShow = !modalShow"
            style="background-color: transparent; border: none; font-size: 25px"
          >
            📷
          </button>
        </div>
        <hr />
        <b-modal id="modal-scoped" v-model="modalShow" size="lg">
          <template #modal-header>
            <h5 class="fw-bold">Select Image</h5>
          </template>

          <template #default>
            <div class="container px-4 py-5 px-md-5">
              <div class="row">
                <div
                  class="col-md-4 profileImg"
                  :class="{ selectProfile: num === new_Img }"
                  @click="selectImg(num)"
                  v-for="num in 12"
                  :key="num"
                >
                  <img :src="getImagePath(num)" style="height: 80%" />
                </div>
              </div>
            </div>
          </template>

          <template #modal-footer>
            <b-button size="sm" variant="primary" @click="changeImg">
              OK
            </b-button>
            <b-button size="sm" variant="danger" @click="cancelImg">
              Cancel
            </b-button>
          </template>
        </b-modal>
      </div>
      <br /><br />
      <div class="left-user" style="font-size: 20px">
        <div v-if="!change_nick">
          <div style="display: flex; justify-content: center">
            <p>UserName |</p>
            <p>&nbsp;&nbsp;&nbsp;{{ new_nickname }}</p>
            <span
              @click="updateNick"
              style="
                cursor: pointer;
                color: rgb(202, 202, 202);
                font-size: 17px;
              "
              >&nbsp;&nbsp;🖌</span
            >
          </div>
        </div>
        <div v-else>
          <b-input v-model="new_nickname" size="sm" @keyup.enter="changeNick" />
          <b-button @click="changeNick" size="sm">Change</b-button>
        </div>
        <div>
          <p>My Id | {{ user.username }}</p>
          <p>E-mail | {{ user.email }}</p>
        </div>
        <br /><br /><br />
        <hr />
        <div style="display: flex; margin-top: 40px; margin-left: 90%">
          <p @click="cancelUp" style="margin-right: 15px; cursor: pointer">
            Back
          </p>
          <p @click="userUpdate" style="cursor: pointer">Update</p>
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
      loggedInUser: this.$store.state.loggedInUser,
      modalShow: false,
      user: [],
      new_nickname: null,
      new_Img: null,
      change_nick: false,
      change_Img: null,
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    getImagePath(userImg) {
      return require(`@/assets/Profile_img0${userImg}.png`);
    },
    getUserData() {
      axios({
        method: "get",
        url: `${API_URL}/account/userinfo/${this.loggedInUser.pk}/`,
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then((res) => {
          this.user = res.data;
          this.new_nickname = this.user.nickname;
          this.change_Img = this.user.profile_img;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateNick() {
      this.change_nick = true;
    },
    changeNick() {
      this.change_nick = false;
    },
    cancelUp() {
      this.$router.push({
        name: "profile",
        params: { account_id: this.user.id },
      });
    },
    selectImg(num) {
      this.new_Img = num;
    },
    changeImg() {
      this.change_Img = this.new_Img;
      this.new_Img = null;
      this.modalShow = false;
    },
    cancelImg() {
      this.new_Img = null;
      this.modalShow = false;
    },
    userUpdate() {
      axios({
        method: "PATCH",
        url: `${API_URL}/account/update/${this.user.id}/`,
        data: {
          nickname: this.new_nickname,
          profile_img: this.change_Img,
        },
        headers: {
          Authorization: `Bearer ${this.accessKey}`,
        },
      })
        .then(() => {
          alert("프로필 업데이트");
          this.$router.push({
            name: "profile",
            params: { account_id: this.user.id },
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.profileImg {
  width: 140px;
  height: 140px;
  border: 1px solid black;
  border-radius: 100%;
  padding: 4px;
  margin: 10px;
  background-color: rgb(247, 250, 211);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
.selectProfile {
  background-color: rgb(207, 255, 207);
}

.main-box {
  width: 90%;
  height: 800px;
  /* border: 2px solid white; */
  margin: auto;
}

.left-image {
  width: 100%;
  height: 350px;
  /* border: 2px solid orange; */
}
.left-user {
  width: 80%;
  margin: auto;
  height: 350px;
  color: rgb(202, 202, 202);
  /* border: 2px solid rgb(228, 223, 223); */
  border-radius: 20px;
  /* background-color: rgb(228, 223, 223); */
  padding: 35px;
  margin-top: -40px;
}
</style>
