<template>
  <ResultData v-if="newData" v-bind:newData="newData"></ResultData>
  <div v-else class="loading-page">
    <img class="paint-spring" src="../assets/images/paintSpring.png" />
    <div class="loading-text">
      <p class="loading-maintext">
        <span style="color: #eeb3ad; font-weight: 1000">'마음 스케치'</span>
        프로젝트는 AI 기술을 통해 유저가 직접 그린 그림을 분석하여 본인의 심리
        및 정서 상태를 파악할 수 있도록 돕고자 제작되었습니다. 본인의 상태가
        심각하다고 판단되거나, 보다 정확한 해석을 알기 위해서는 전문 의료진을
        찾아주세요.
      </p>
      <p class="member-text-header">프로젝트 참여 인원:</p>
      <p class="member-text">
        Front-End: 이윤영, 최건 <br />
        Back-End: 양채린, 황혜수, 백소미 <br />
        AI: 이수민, 이겸희 <br />Design: 이가윤
      </p>
      <img class="loading-img" src="../assets/images/heart.png" />
    </div>
    <p class="touch-text1">잠시만 기다려주세요...</p>
  </div>
</template>

<script>
import ResultData from "../views/Result/ResultData.vue";
export default {
  name: "LoadingPage",
  components: { ResultData },
  props: ["newData"],
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.loading-page {
  height: calc(var(--vh, 1vh) * 100);
  background-image: url("../assets/images/night.jpg");
  overflow: hidden;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  font-family: korFont3;
}
.loading-text {
  width: 70%;
  font-family: korFont3;
  display: flex;
  flex-direction: column;
  padding-top: 60px;
  display: inline-block;
  align-items: center;
}
.loading-maintext {
  font-size: 18px;
  text-align: left;
  line-height: 2;
  padding-top: 30px;
  padding-bottom: 10px;
}
.member-text-header {
  font-size: 21px;
  font-family: korFont3;
  padding-top: 20px;
  padding-bottom: 20px;
  font-family: korFont3;
  font-weight: 1000;
}
.member-text {
  font-size: 20px;
  font-family: korFont3;
  line-height: 1.3;
}
.touch-text1 {
  color: #dededeb9;
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
  text-align: center;
  bottom: 7%;
  font-size: 17px;
  animation: blinker 2s linear infinite;
}
.paint-spring {
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
.loading-img {
  width: 45px;
  display: inline-block;
  margin-top: 30px;
}
</style>
