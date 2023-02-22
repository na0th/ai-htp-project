<template>
  <div class="desktop-scene">
    <div class="desktop-text">
      <img class="icon1" src="../assets/images/icon1.png" />
      <p class="title-text"><span style="color: #eba090">마음</span>스케치</p>
      <p class="title-subtext">내가 그린 그림으로 확인해보는 나의 심리</p>
      <img class="qrcode" src="../assets/images/QR.svg.png" />
    </div>
  </div>
</template>
<script>
export default {
  name: "DesktopScene",
  components: {},
  data() {
    return {
      sampleData: "",
    };
  },
};
</script>
<style scoped>
.desktop-scene {
  height: 100vh;
  background-image: url("../assets/images/desktop1.png");
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  color: black;
}
.desktop-text {
  position: absolute;
  top: 15%;
  left: 0;
  right: 0;
}
.title-text {
  font-family: korFont1;
  font-size: 55px;
}
.title-subtext {
  font-family: korFont3;
  font-size: 25px;
  margin-top: 20px;
}
.icon1 {
  margin-bottom: 30px;
  width: 100px;
}
.qrcode {
  width: 100px;
  margin-top: 30px;
}
</style>
