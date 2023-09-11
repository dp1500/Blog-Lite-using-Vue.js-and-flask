<template>
    <div>
        <p>{{ msg }}</p>
        <div>
            <button @click="sendPostRequest">Send POST Request</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name:'SharkTest',
    data() {
        return {
            msg: ""
        };
    },
    methods: {
        getResponseTest(){
            const path = 'http://localhost:5000/shark'
            axios.get(path)
            .then((resp) => {
                console.log(resp.data)
                this.msg = resp.data;
            })
            .catch((err) => {
                console.log(err);
            });
        },
    

    sendPostRequest() {
        console.log('sendPostRequest method called');
            const path = 'http://localhost:5000/shark'
            axios.post(path)
            .then(resp => {
                this.msg = resp.data;
                console.log('POST request sent successfully');
            })
            .catch(error => {
                console.log(error);
            });
        },
    },

    created(){
        this.getResponseTest()
    }
}
</script>