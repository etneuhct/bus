<template>
  <div id="app">
    <nav class="blue">
      <div class="nav-wrapper">
        <a href="#" class="brand-logo center">BusFit!</a>
      </div>
    </nav>
    <div id="scorecard">
      <div class="card blue">
        <div class="card-content white-text">
          <span class="left">
            <img class="star" src="./assets/star.png" alt="Score" />
          </span>
          <span class="right">
            {{score}}
          </span>
        </div>
      </div>
    </div>
    <div id="coach">
      <img :src="animation_file" alt="Le coach arrive..">
    </div>
    <animated-bounce-in-up>
      <div class="bulle-point green-text" v-if="goodAttemptDetected">
        +1
      </div>
    </animated-bounce-in-up>
    <animated-bounce-in-up>
      <div class="container-thought">
        <p class="thought" v-if="tooClose">
          Tenez-vous bien dans mon champ de vision pour jouer !
        </p>
      </div>
    </animated-bounce-in-up>
  </div>
</template>

<script>
export default {
  name: 'app',
  sockets: {
    connect: function(){
      console.log('socket connected');
    },
    data: function(data){
      console.log('io.emit("data")', data);
      this.tooClose = !!data.tooClose;
      if (data.drill){
        this.totalScore += data.drill != this.currentDrill.drill ? 
          this.currentDrill.counter : 0;
        this.currentDrill = data;
      }
    }
  },
  data:  function() {
    return {
      gameStarted: false,
      goodAttemptDetected: false,
      attemptDetected: false,
      tooClose: false,
      currentDrill: null,
      totalScore: 0
    }
  },
  computed: {
    animation_file: function(){
      return require('./assets/' + (this.currentDrill ? this.currentDrill.drill : 'jumping_jacks') + '.gif');
    },
    score: function(){
      var score = this.currentDrill ? this.currentDrill.counter : 0;
      score += this.totalScore;
      return score;
    }
  },
  watch: {
    goodAttemptDetected: function(){
      var _self = this;
      this.bubbleTimeout && clearTimeout(this.bubbleTimeout);
      if (this.goodAttemptDetected){
        this.bubbleTimeout = setTimeout(function(){
          _self.goodAttemptDetected = false;
        }, 700);
      }
    },
  },
  beforeDestroy: function(){
    this.bubbleTimeout && clearTimeout(this.bubbleTimeout);
  }
}
</script>

<style>
body, html {
  font-size: 16px;
  height: 100%;
  min-height: 100%;
  overflow: hidden;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  position: absolute;
  top: 0;
}

.container-thought {
  position: absolute;
  left: 30%;
  top: 60px;
}

#scorecard {
  height: 200px;
  text-align: right;
  width: 100%;
}

#scorecard .card {
  background: linear-gradient(to bottom right, #5967C3, #83cedc);
  font-size: 2.5em;
  max-width: 40%;
  min-width: 15%;
  opacity: 0.92;
  padding-bottom: .6em;
  position: absolute;
  top: 30px;
  right: 5%;
  width: 300px;
  z-index: 2;
}

#scorecard .card-content {
  padding-bottom: 1.5em;
}

#scorecard .star {
  max-height: 70px;
  position: relative;
  top: -10px;
}

#coach {
  text-align: center;
  position: relative;
  top: -9em;
  width: 100%;
}

#coach img {
  max-height: 90%;
  height: auto;
}

.bulle-point {
  font-size: 3em;
  font-weight: bold;
  position: absolute;
  top: 80px;
  right: 80px;
  z-index: 4
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}


</style>
