<template>
  <div class="header">
    <img src="../assets/Logo.svg" alt="logo" id="logo" />
  </div>
  <transition appear appear-active-class="fade-enter-active" >
    <div id="info">
        <div id="card" class="shadow">
            <span>404</span>
            <h1>Oops! Page Not found</h1>
            <div class="btn shadow" @click.prevent="redirect">Go back home</div>
        </div>
    </div>
  </transition>    
</template>

<script>
export default {
    title:"404 not found!",
    methods:{
        redirect(){
            this.$router.push('/')
        }
    }
}
</script>
<style scoped>
#info{
    width: 100%;
    height: calc(100vh - 200px);
    display: flex;
    justify-content:center;
    align-items: center;
    
}
#card{
    background-color: white;
    width: 30%;
    min-width: 250px;
    height: 60%;
    border-radius: 29px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 40px;
}
#card span{
    text-align: center;
    animation: 1s ease-out 0s 1 slideInFromBottom;
  background: -webkit-linear-gradient(
    -90deg,
    #653277 0%,
    #505690 15.62%,
    #5f679c 33.33%,
    #6e79a9 48.44%,
    #8b9bc1 65.62%,
    #c7e1f3 85.42%
  );
  background: -webkit-linear-gradient(
    -90deg,
    #653277 0%,
    #505690 15.62%,
    #5f679c 33.33%,
    #6e79a9 48.44%,
    #8b9bc1 65.62%,
    #c7e1f3 85.42%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 5rem;
}
#info h1{
    font-size: 2rem;
    text-align: center;
    color: #505690;
}
#info h2{
    text-align: center;
    color: grey;
    font-size: 1.5rem;
    padding: 0px 20px;
}
.shadow {
  box-shadow: 0 3px 5.2px rgba(0, 0, 0, 0.02),
    0 7.2px 12.5px rgba(0, 0, 0, 0.028), 0 13.6px 23.5px rgba(0, 0, 0, 0.035),
    0 24.3px 42px rgba(0, 0, 0, 0.042), 0 45.5px 78.5px rgba(0, 0, 0, 0.05),
    0 109px 188px rgba(0, 0, 0, 0.07);
}
/* initial transition */
.fade-enter-active {
  animation: go 0.5s ease;
}

@keyframes go {
  0% {
    transform: scale(0.70);
    opacity: 20%;
  }
  50%{
    transform: scale(1.05);
    opacity: 100%;
  }
  100% {
    transform: scale(1);
    opacity: 100%;
  }
}
/* button */
.btn {
  text-decoration: none;
  color: white;
  background-color: #505690;
  padding: 20px;
  border-radius: 13px;
  font-size: 2rem;
  text-align: center;
  margin: 0 10px 10px 10px;

  
}

.btn:hover {
  transform: scale(1.03);
}

.btn:active {
  transform: scale(0.98);
}

</style>