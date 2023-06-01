<template>
  <div class="d">
    <div class="main-box">
      <div class="header-box">
        <div class="h-title">
          <h1>Recommend</h1>
        </div>
        <br />
        <div class="h-content">
          <div><p>&nbsp;&nbsp; &nbsp;&nbsp;</p></div>
          <div style="align-items: center">
            <h5>
              {{ user.nickname }} 님께서 선호하시는 장르를 분석하여 시스템이
              추천하는 영화입니다.
            </h5>
          </div>
          <div class="h-random">
            <button
              @click="re"
              style="
                border: none;
                background-color: transparent;
                font-size: 40px;
                margin-right: 45px;
              "
            >
              🎲
            </button>
          </div>
        </div>
      </div>
      <br /><br /><br />
      <div class="card-box">
        <div
          class="card"
          v-for="(card, index) in cards"
          :key="index"
          @click="flipCard(index)"
        >
          <div class="b-image">
            <div style="width: 95%">
              <img
                :src="random_4[index][0]"
                style="width: 100%; border-radius: 8px"
              />
            </div>
            <h5 style="margin-top: 15px; color: white">
              {{ random_4[index][1] }}
            </h5>
          </div>
          <div class="front" :class="{ flipped: card.flipped }"></div>
          <div class="back"></div>
        </div>
      </div>
      <br /><br /><br /><br />
      <h1 style="color: white; text-align: left; margin-left: 50px">
        장르별 추천
      </h1>
      <br /><br />
      <h5 style="color: white; text-align: left; margin-left: 50px">
        액션 || 애니메이션 || 코미디 || 판타지 || 로맨스
      </h5>
      <hr style="color: rgb(187, 185, 185); margin-left: 50px; width: 95%" />
      <div class="genre-box">
        <div class="g_1">
          <vue-swing ref="vueswing" :config="config" @throwout="onThrowout">
            <div v-for="card in g_c_1" :key="card" class="card_">
              <img :src="card" class="card_1" />
            </div>
          </vue-swing>
        </div>
        <div class="g_2">
          <vue-swing ref="vueswing" :config="config" @throwout="onThrowout">
            <div v-for="card in g_c_2" :key="card" class="card_2">
              <img :src="card" class="card_2_2" />
            </div>
          </vue-swing>
        </div>
        <div class="g_3">
          <vue-swing ref="vueswing" :config="config" @throwout="onThrowout">
            <div v-for="card in g_c_3" :key="card" class="card_3">
              <img :src="card" class="card_3_2" />
            </div>
          </vue-swing>
        </div>
        <div class="g_4">
          <vue-swing ref="vueswing" :config="config" @throwout="onThrowout">
            <div v-for="card in g_c_4" :key="card" class="card_4">
              <img :src="card" class="card_4_2" />
            </div>
          </vue-swing>
        </div>
        <div class="g_5">
          <vue-swing ref="vueswing" :config="config" @throwout="onThrowout">
            <div v-for="card in g_c_5" :key="card" class="card_5">
              <img :src="card" class="card_5_2" />
            </div>
          </vue-swing>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueSwing from "vue-swing";
import axios from "axios";
const API_URL = "http://127.0.0.1:8000/GoonManDu";
export default {
  components: { VueSwing },
  data() {
    return {
      accessKey: this.$store.state.accessKey,
      g_data: this.$store.state.rec_genres,
      user_g_data: null,
      user: [],
      URL: [],
      random_4: [],
      g_c_1: [],
      g_c_2: [],
      g_c_3: [],
      g_c_4: [],
      g_c_5: [],

      cards: [
        { flipped: false },
        { flipped: false },
        { flipped: false },
        { flipped: false },
      ],
      config: {
        allowedDirections: [
          VueSwing.Direction.UP,
          VueSwing.Direction.DOWN,
          VueSwing.Direction.LEFT,
          VueSwing.Direction.RIGHT,
        ],
        minThrowOutDistance: 250,
        maxThrowOutDistance: 300,
      },
      cards_: [
        "A",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
      ],
      genreCard: null,
    };
  },
  created() {
    if (this.$store.state.rec_genres === null) {
      alert("영화 추천을 위해 선호하시는 영화를 알려주세요🧡");
      this.$router.push({ name: "main" });
    }
    this.getUserData();
    // console.log(this.$store.state.rec_genres);
    const tmp = [];
    for (let i = 0; i < this.g_data.length; i++) {
      var st = "";
      for (let j = 1; j < this.g_data[i].length; j++) {
        if (
          this.g_data[i][j] != "]" &&
          this.g_data[i][j] != "," &&
          this.g_data[i][j] != ""
        ) {
          st += this.g_data[i][j];
        } else {
          tmp.push(Number(st));
          st = "";
        }
      }
    }
    function getMode(array) {
      // 1. 출연 빈도 구하기
      const counts = array.reduce((pv, cv) => {
        pv[cv] = (pv[cv] || 0) + 1;
        return pv;
      }, {});

      // 2. 최빈값 구하기
      const keys = Object.keys(counts);
      let mode = keys[0];
      keys.forEach((val, idx) => {
        if (counts[val] > counts[mode]) {
          mode = val;
        }
      });

      return mode;
    }

    this.user_g_data = getMode(tmp);

    // DB 100-200 돌면서 찾아오기
    axios
      .get(`${API_URL}/movies/`)
      .then((res) => {
        const tmp = [];
        const genre = [];
        const tmp_g_1 = [];
        const tmp_g_2 = [];
        const tmp_g_3 = [];
        const tmp_g_4 = [];
        const tmp_g_5 = [];
        for (let i = 0; i < res.data.length; i++) {
          // console.log(res.data[i].genre_ids)
          if (res.data[i].genre_ids.includes(String(this.user_g_data))) {
            tmp.push([
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path,
              res.data[i].title,
            ]);
          }
          // 각 장르 별로 포스터 사진 넣기
          if (res.data[i].genre_ids.includes(this.genreCard[0].id)) {
            tmp_g_1.push(
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path
            );
          }

          if (res.data[i].genre_ids.includes(this.genreCard[1].id)) {
            tmp_g_2.push(
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path
            );
          }

          if (res.data[i].genre_ids.includes(this.genreCard[2].id)) {
            tmp_g_3.push(
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path
            );
          }

          if (res.data[i].genre_ids.includes(this.genreCard[3].id)) {
            tmp_g_4.push(
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path
            );
          }

          if (res.data[i].genre_ids.includes(this.genreCard[4].id)) {
            tmp_g_5.push(
              "https://image.tmdb.org/t/p/w500" + res.data[i].poster_path
            );
          }
        }
        this.URL = tmp;

        // 랜덤으로 10장 뽑기-1
        var new_random = [];
        var a = tmp_g_1.length;
        while (tmp_g_1.length > a - 10) {
          var movenum = tmp_g_1.splice(
            Math.floor(Math.random() * tmp_g_1.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.g_c_1 = new_random;

        // 랜덤으로 10장 뽑기-2
        var new_random = [];
        var a = tmp_g_2.length;
        while (tmp_g_2.length > a - 10) {
          var movenum = tmp_g_2.splice(
            Math.floor(Math.random() * tmp_g_2.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.g_c_2 = new_random;

        // 랜덤으로 10장 뽑기-3
        var new_random = [];
        var a = tmp_g_3.length;
        while (tmp_g_3.length > a - 10) {
          var movenum = tmp_g_3.splice(
            Math.floor(Math.random() * tmp_g_3.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.g_c_3 = new_random;

        // 랜덤으로 10장 뽑기-4
        var new_random = [];
        var a = tmp_g_4.length;
        while (tmp_g_4.length > a - 10) {
          var movenum = tmp_g_4.splice(
            Math.floor(Math.random() * tmp_g_4.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.g_c_4 = new_random;

        // 랜덤으로 10장 뽑기-5
        var new_random = [];
        var a = tmp_g_5.length;
        while (tmp_g_5.length > a - 10) {
          var movenum = tmp_g_5.splice(
            Math.floor(Math.random() * tmp_g_5.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.g_c_5 = new_random;

        // 랜덤 돌리기
        var new_random = [];
        var a = this.URL.length;
        while (this.URL.length > a - 4) {
          var movenum = this.URL.splice(
            Math.floor(Math.random() * this.URL.length),
            1
          )[0];
          new_random.push(movenum);
        }
        this.random_4 = new_random;
      })
      .catch((err) => {
        console.log(err);
      });

    // 장르 일단 가져오기
    axios({
      method: "GET",
      url: "https://api.themoviedb.org/3/genre/movie/list?language=ko",
      headers: {
        accept: "application/json",
        Authorization:
          "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q",
      },
    })
      .then((response) => {
        // 액션28[0], 애니메이션16[2], 코미디 35[3], 판타지14[8], 로맨스10749[13]
        const tmp_g_card = [];
        tmp_g_card.push(response.data.genres[0]);
        tmp_g_card.push(response.data.genres[2]);
        tmp_g_card.push(response.data.genres[3]);
        tmp_g_card.push(response.data.genres[8]);
        tmp_g_card.push(response.data.genres[13]);

        this.genreCard = tmp_g_card;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    getUserData() {
      axios({
        method: "get",
        url: `${API_URL}/account/userinfo/${this.$store.state.loggedInUser.pk}/`,
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
    flipCard(index) {
      this.cards[index].flipped = !this.cards[index].flipped;
    },
    onThrowout({ target, throwDirection }) {
      console.log(`Threw out ${target.textContent}!`);
    },
    re() {
      // 랜덤을 돌려서 나오게 하기
      var new_random = [];
      var a = this.URL.length;
      while (this.URL.length > a - 4) {
        var movenum = this.URL.splice(
          Math.floor(Math.random() * this.URL.length),
          1
        )[0];
        new_random.push(movenum);
      }
      this.random_4 = new_random;
      console.log(this.random_4);

      this.cards = [
        { flipped: false },
        { flipped: false },
        { flipped: false },
        { flipped: false },
      ];
    },
  },
};
</script>

<style scoped>
.card-box {
  display: flex;
  justify-content: space-around;
}

.card {
  width: 300px;
  height: 500px;
  perspective: 1000px;
  cursor: pointer;
  border-radius: 8px;
  background: transparent;
}

.card_ {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 350px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 250px;
  position: absolute;
  left: 190px;
  top: 1150px;
}

.card_1 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 200px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  position: absolute;
}

.card_2 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 350px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 250px;
  position: absolute;
  left: 520px;
  top: 1150px;
}

.card_2_2 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 200px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  position: absolute;
}

.card_3 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 350px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 250px;
  position: absolute;
  left: 850px;
  top: 1150px;
}

.card_3_2 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 200px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  position: absolute;
}
.card_4 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 350px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 250px;
  position: absolute;
  left: 1180px;
  top: 1150px;
}

.card_4_2 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 200px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  position: absolute;
}

.card_5 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 350px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 250px;
  position: absolute;
  left: 1510px;
  top: 1150px;
}

.card_5_2 {
  align-items: center;
  background-color: transparent;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  font-size: 72px;
  height: 200px;
  justify-content: center;
  left: calc(50% - 100px);
  top: calc(50% - 100px);
  width: 200px;
  position: absolute;
}

.front,
.back {
  width: 100%;
  height: 100%;
  position: absolute;
  transition: transform 0.8s;
  backface-visibility: hidden;
}

.front {
  background-color: #6d6b6b;
  border-radius: 8px;
}

.back {
  background-color: white;
  transform: rotateY(140deg);
}

.flipped {
  transform: rotateY(140deg);
}

.d {
  padding: 30px;
  padding-bottom: 600px;
}
.main-box {
  width: 90%;
  /* border: 2px solid white; */
  margin: 60px auto 60px auto;
  padding: 10px;
}
.header-box {
  width: 100%;
  /* border: 2px solid white; */
}

.h-title {
  color: white;
}

.h-content {
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-box {
  display: flex;
  width: 100%;
  /* border: 2px solid pink; */
  justify-content: space-around;
}

.genre-box {
  width: 100%;
  /* border: 2px solid pink; */
}

.g_card {
  width: 100%;
  height: 100%;
}
</style>
