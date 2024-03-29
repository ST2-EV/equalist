<template>
  <div class="header">
    <img src="../assets/Logo.svg" alt="logo" id="logo" />
  </div>
  <transition appear appear-active-class="fade-enter-active" >
    <div id="info">
        <div id="card" class="shadow">
            <h1>Yayy! You have been added to the room!</h1>
            <h2>Ask the host for the playlist link.</h2>
        </div>
    </div>
  </transition>    
</template>
<script>
export default {
  title: "Success!!"
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
    width: 70%;
    height: 60%;
    border-radius: 29px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 40px;
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
</style>