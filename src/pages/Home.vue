<template>
    <div>
        <Test/>
        <Hitokoto/>
    </div>
</template>

<script>
import Test from "@/components/Test";
import Hitokoto from "@/components/Hitokoto";
import Nav from "@/components/Nav";
    export default {
        name:'Home',
        components:{
            Test,
            Hitokoto,
            Nav
        }
    }
</script>

<style  scoped>

</style>