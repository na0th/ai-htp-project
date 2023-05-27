<template>
  <div class="results-data">
    <h1 class="userName">{{ username }}님의 결과입니다.</h1>
    <div>
      <img
        class="characterImage"
        :src="getImageUrl(character_id)"
        alt="Character Image"
      />
    </div>
    <div class="characterName" >
      {{ character_name[character_id-1] }}
    </div>
    <div>
      <canvas id="myChart" width="25" height="25"></canvas>
    </div>

    <img class="paint-spring" src="../../assets/images/paintSpring.png" />
    <button class="showDetailBtn" @click="showDetail">상세보기</button>
    <transition name="fade">
      <div v-if="showResults" class="details" :class="{ open: showDetails }">
        <div class="first-result">
          <h1 class="first-result-title">{{ username }}님의 나무 그림</h1>
          <img width="200" height="300" :src="newData.image1" alt="image" />
          <div class="result-texts">
            <div v-for="(treeAttributes, key1) in tree" :key="key1">
              <br />
              <p class="treeAttributes">{{ key1 }}</p>
              <template v-for="(treeFeatures, key2) in treeAttributes">
                <div
                  v-if="treeFeatures !== null && treeFeatures !== undefined"
                  :key="key2"
                >
                  <li class="treefeatures">
                    {{ key2 }}
                  </li>
                  <p class="treevalues">
                    {{ treeFeatures }}
                  </p>
                </div>
              </template>
            </div>
          </div>
        </div>
        <div class="second-result">
          <h1 class="first-result-title">{{ username }}님의 집 그림</h1>
          <img width="200" height="300" :src="newData.image2" alt="image" />
          <div class="result-texts">
            <div v-for="(homeAttributes, key1) in home" :key="key1">
              <br />
              <p class="treeAttributes">{{ key1 }}</p>
              <template
                v-for="(homeFeatures, key2) in homeAttributes"
                :key="key2"
              >
                <div
                  v-if="homeFeatures !== null && homeFeatures !== undefined"
                  :key="key2"
                >
                  <li class="treefeatures">
                    {{ key2 }}
                  </li>
                  <p class="treevalues">
                    {{ homeFeatures }}
                  </p>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <br />
    <p class="share-btns-text">공유하기</p>
    <div class="share-btns">
      <a id="kakaotalk-sharing-btn" href="javascript:;">
        <img
          src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
          alt="카카오톡 공유 보내기 버튼"
          class="kakaotalk-btn"
          @click="kakaoLink"
        />
      </a>
      <div class="clipboard-copy">
        <font-awesome-icon
          class="copylink-btn"
          @click="urlCopy"
          icon="fa-solid fa-link"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
export default {
  name: "ResultData",
  props: ["newData"],
  components: {},
  data() {
    return {
      character_name:['공격적인 돼지바 프라푸치노','노른자가 두 개 띄워진 쌍화탕','샷 6번 추가한 공격적인 아메리카노',
      '자존감 높은 1리터 쌍화탕','샷 6번 추가한 따뜻한 라떼','혼자 있기 좋아하는 자몽 허니 블랙티','따뜻한 아이스 아메리카노',
      '인정이 필요한 민트 초코 라떼','미지근한 카모마일티','자신감이 넘치는 유니콘 프라푸치노','얼음이 녹아버린 아샷추','톡 쏘는 블루레몬에이드',
      '휘핑 가득 따뜻한 민트초코라떼','펄 추가 아이스아메리카노','행복한 민트초코프라푸치노','혼자가 된 제주 유기농 감귤 주스','거품 뺀 카푸치노','초코쉐이크가 되고싶은 밀크쉐이크',
      '따뜻한 숏라떼','수줍은 복숭아 아이스티'
      ],
      username: null,
      tree: null,
      home: null,
      graph: [],
      character_id: null,
      showResults: false,
    };
  },
  methods: {
    showDetail() {
      this.showResults = !this.showResults;
    },
    getImageUrl(value) {
      return require(`../../assets/images/${value}.png`);
    },
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
    urlCopy() {
      this.$copyText("http://192.168.219.103:8080/").then(() => {
        alert("클립보드에 성공적으로 복사되었습니다.");
      });
    },
  },
  created() {
    this.username = this.newData.name;
    this.tree = this.newData.tree_result;
    this.home = this.newData.house_result;
    this.graph = this.newData.graph;
    this.character_id = this.newData.character;
  },
  mounted() {
    console.log("Component mounted.");
    const ctx = document.getElementById("myChart");
    const myChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: ["공격성", "사회불안", "우울", "대인회피", "낮은 자존감"],
        datasets: [
          {
            label: "수치",
            data: this.graph,
            backgroundColor: [
              // "rgba(255, 99, 132, 0.2)",
              // "rgba(54, 162, 235, 0.2)",
              // "rgba(255, 206, 86, 0.2)",
              // "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              // "rgba(54, 162, 235, 1)",
              // "rgba(255, 206, 86, 1)",
              // "rgba(75, 192, 192, 1)",
              // "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 2,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 10,
            bottom: 10,
            left: 10,
            right: 10,
          },
        },
        plugins: {
          legend: {
            display: false, // Hide the legend
          },
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 1,
            angleLines: {
              display: false,
            },
            ticks: {
              display: false,
            },
          },
        },
      },
    });
    myChart;
  },
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
  border-bottom: 1px solid #ccc;
  margin-bottom: 20px;
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
  margin-bottom: 20px;
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
  font-family: korFont2;
  margin-bottom: 10px;
  font-size: 20px;
}
.share-btns {
  margin-bottom: 15px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 15px;
}
.kakaotalk-btn {
  height: 40px;
}
.copylink-btn {
  height: 30px;
}
.clipboard-copy {
  display: inline-block;
}
.characterImage {
  width: 160px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
}
#myChart {
  width: 250px;
}
.showDetailBtn {
  background-color: #3498db; /* Set the button background color */
  padding: 8px 16px; /* Add padding to the button */
  color: #ffffff; /* Set the button text color */
  border: none; /* Remove the button border */
  cursor: pointer; /* Show pointer cursor on hover */
  border-radius: 25px;
  margin-bottom: 25px;
  font-family: korFont2;
}
.characterName {
  font-size: 18px;
  font-weight: bold;
  margin-top: 10px;
  padding: 10px;
  border: 2px solid pink;
  border-radius: 10px;
  display: inline-block;
  max-width: 320px;
  word-wrap: break-word;
}

</style>
