<template>
  <div class="results-data">
    <img class="paint-spring" src="../../assets/images/paintSpring.png" />
    <h1 class="userName">{{ username }}님의 결과입니다.</h1>

    <div class="first-result">
      <h1 class="first-result-title">{{ username }}님의 나무 그림</h1>
      <img width="200" height="300" :src="data.image1" alt="image" />
      <div class="result-texts">
        <div v-for="(treeAttributes, key1) in tree" :key="key1">
          <br />
          <p class="treeAttributes">{{ key1 }}</p>

          <div v-for="(treeFeatures, key2) in treeAttributes" :key="key2">
            <li class="treefeatures">{{ key2 }}</li>
            <p class="treevalues">{{ treeFeatures }}</p>
          </div>
        </div>
      </div>
    </div>
    <br />
    <div class="second-result">
      <h1 class="first-result-title">{{ username }}님의 집 그림</h1>
      <img width="200" height="300" :src="data.image2" alt="image" />
      <div class="result-texts">
        <div v-for="(homeAttributes, key1) in home" :key="key1">
          <br />
          <p class="treeAttributes">{{ key1 }}</p>

          <div v-for="(homeFeatures, key2) in homeAttributes" :key="key2">
            <li class="treefeatures">{{ key2 }}</li>
            <p class="treevalues">{{ homeFeatures }}</p>
          </div>
        </div>
      </div>
    </div>
    <br />
    <div class="share-btns">
      <p class="share-btns-text">공유하기</p>
      <a id="kakaotalk-sharing-btn" href="javascript:;">
        <img
          src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
          alt="카카오톡 공유 보내기 버튼"
          class="kakaotalk-btn"
          @click="kakaoLink"
        />
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultData",
  props: ["data"],
  components: {},
  data() {
    return {
      username: null,
      tree: null,
      home: null,
    };
  },
  methods: {
    kakaoLink() {
      window.Kakao.Share.createDefaultButton({
        container: "#kakaotalk-sharing-btn",
        objectType: "feed",
        content: {
          title: "마음스케치",
          description: "#AI심리검사 #그림심리검사",
          imageUrl:
            "http://k.kakaocdn.net/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
          link: {
            // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
            mobileWebUrl: "https://developers.kakao.com",
            webUrl: "https://developers.kakao.com",
          },
        },
        social: {
          likeCount: 123,
          commentCount: 456,
          sharedCount: 789,
        },
        buttons: [
          {
            title: "웹으로 보기",
            link: {
              mobileWebUrl: "https://developers.kakao.com",
              webUrl: "https://developers.kakao.com",
            },
          },
        ],
      });
    },
  },
  setup() {},
  created() {
    this.username = this.data.username;
    this.tree = this.data.tree;
    this.home = this.data.home;
  },
  mounted() {},
};
</script>

<style>
.results-data {
  display: inline-block;
  font-family: korFont2;
  background-color: #ffffff;

  background-size: cover;
  /* background-repeat: no-repeat; */
  background-position: center center;
  color: black;
  font-family: korFont1;
  width: 100%;
  height: auto !important;
}
.userName {
  font-size: 28px;
  margin-top: 15%;
  font-family: korFont3;
}
.first-result {
  margin-top: 50px;
}

.first-result-title {
  font-size: 20px;
  margin-bottom: 10px;
  font-family: korFont3;
}
.first-image {
  margin-top: 25px;
  width: 250px;
}
.first-result-text {
  width: 80%;
  margin: 50px auto;
}
.result-texts {
  text-align: left;
  font-family: korFont2;
  width: 80%;
  display: inline-block;
}
.treeAttributes {
  font-weight: 1000;
  font-size: 22px;
  margin-bottom: 15px;
}
.treefeatures {
  font-size: 18px;
  margin-bottom: 8px;
}
.treevalues {
  font-size: 18px;
  margin-bottom: 15px;
  line-height: 1.2;
}
.share-btns-text {
  font-family: korFont1;
  margin-bottom: 10px;
}
.share-btns {
  margin-bottom: 15px;
}
.kakaotalk-btn {
  width: 50px;
}
</style>
