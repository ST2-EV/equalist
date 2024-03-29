<template>
        <div class="header">
            <img src="@/assets/Logo.svg" alt="logo" id="logo" />
        </div>
          <section id="hero">
              <h1>Create a playlist that all your friends love!</h1>
              <div id="btns">
                  <a class="btn-alt shadow" href="#" title="Create Now" @click.prevent="createRoom">
                      <span v-if="!loading">Create Now</span>
                      <div :class="[loading ? 'spinner' : '']"></div>
                  </a>
                  
                  <a class="btn shadow" href="#info" title="Learn More">Learn More</a>
              </div>
          
          </section>
            
          <section id="info">
                  <h1>How to make that awesome playlist?</h1>
                  <a class="btn-alt-2 shadow" href="#" title="Create Now" @click.prevent="createRoom">
                     <span v-if="!loading">Create Now</span>
                     <div :class="[loading ? 'spinner' : '']"></div>
                  </a>
                  <p class="step"><span>1</span>Hit "Create Now" to login with spotify and create your room.</p>
                  <p class="step"><span>2</span>Share the room's link with your friends to add them to the room.</p>
                  <p class="step"><span>3</span>Once all your friends join you can hit create playlist and voila, the perfect playlist!</p>
                  
          </section>
</template>

<script>
import { options } from '@/assets/backend-url'

export default {
  title: "Equalist",
   data () {
      return {
          loading: false
      }
  },
  methods: {
    createRoom() {
        this.loading = true
        window.location = options.url+'oauth/none'
    },
  },
  beforeCreate() {
    if (localStorage.getItem('user_id') !== null) {
        this.$router.push('waiting-room')
    }else{
        localStorage.clear()
    }
  },
   mounted(){
      this.addToAnalytics('home')
  }
}
</script>

<style scoped>
/* spinner */

@keyframes spin {
  to {transform: rotate(360deg);}
}
 
.spinner {
  content: '';
  box-sizing: border-box;
  width: 25px;
  height: 25px;
  margin: 0 auto;
  border-radius: 50%;
  border: 2px solid #ccc;
  border-top-color: #323377;
  animation: spin .6s linear infinite;
}


/* Hero */
#hero {
    height: calc(100vh - 100px);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

#hero h1{
    max-width: 80%;
    text-align: center;
    color: white;
    font-size: 2em;
    margin: 15px;
}

.btn{
    text-decoration: none;
    color: white;
    background-color: #323377;
    padding: 20px;
    border-radius: 7px;
    font-size: 1.4em;
    margin: 5px;
    text-align: center;
    flex-basis: 190px;
}

.btn-alt{
    text-decoration: none;
    color: #323377;
    background-color: white; 
    padding: 20px;
    border-radius: 7px;
    font-size: 1.4em;
    margin: 5px;
    text-align: center;
    flex-basis: 190px;
}

.btn:hover {
	transform: scale(1.03);
}

.btn:active {
	transform: scale(0.98);
}

.btn-alt:hover {
	transform: scale(1.03);
}

.btn-alt:active {
	transform: scale(0.98);
}

.btn-alt-2:hover {
	transform: scale(1.03);
}

.btn-alt-2:active {
	transform: scale(0.98);
}

.shadow{
    box-shadow:
    0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028),
    0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042),
    0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
  
}

#btns{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    width: 100%;
    height: 10%;
}

/* main hero's size needto be large fro bigger screens */
@media only screen   
and (min-device-width : 768px)   
{ #hero h1{
    max-width: 80%;
    text-align: center;
    color: white;
    font-size: 3em;
    margin: 15px;
}}  

/* Info page */
#info {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 50px;
}

#info h1{
    color: white;
    font-size: 2em;
    text-align: center;
    padding-left:0.5em;
    padding-right: 0.5em;
}

#info p{
    background-color: white;
    padding: 30px;
    width: 50%;
    border-radius: 7px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    
}

.btn-alt-2{
    text-decoration: none;
    color: #323377;
    background-color: white; 
    padding: 20px;
    border-radius: 7px;
    font-size: 1.4em;
    margin: 5px;
    text-align: center;
}

#info p span{
    background: -webkit-linear-gradient(-90deg, #653277 0%, #505690 15.62%, #5F679C 33.33%, #6E79A9 48.44%, #8B9BC1 65.62%, #C7E1F3 85.42%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    padding-right: 20px;
}


@media only screen   
and (min-device-width : 768px)   
{ #info p{
    font-size: 1.4rem;
    }

    #info {
        padding-bottom: 100px;
    }

}  
</style>
