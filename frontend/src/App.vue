<template>
    <router-view />
</template>

<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap');

html { 
    background-image: linear-gradient(180deg, #323377 0%, #505690 21.88%, #5F679C 40.63%, #6E79A9 62.5%, #8B9BC1 79.17%, #C7E1F3 100%);
    background-repeat: no-repeat;
    background-position:center;
    background-attachment: fixed;
    font-family: 'Montserrat', sans-serif;
    height: 100%;
}
body{
    height: 100%;
    margin:0;
    padding: 0;
}

/* Header Portion */
.header{
    width: 100%;
    display: flex;
    justify-content: center;
}

#logo{
    height: 40px;
    padding-top: 30px;
}


</style>
