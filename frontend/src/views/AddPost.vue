
<template>

    <div class = 'AddPost'>
        <NavBar/> <!-- use the Navbar component here -->
<div class="col-md-6 offset-md-3 mt-5">

<h2>Add a Blog/Post</h2>
<br>
<form accept-charset="UTF-8" enctype="multipart/form-data" @submit.prevent="sendNewBlogData">
  <div class="form-group" >
    <label for="title" >Enter a title for your post</label>
    <input type="text" name="title" class="form-control" id="title" placeholder="Title" v-model="title" required>
  </div>
  <br>
 
  <div class="form-group">
   <label for="description">Add some description of your post</label>
    <textarea id="description" name="description" rows="7" cols="101" v-model="description"></textarea>
  </div>
  <br>
  <div class="form-group">
    <label for="csv">Upload a CSV file</label>
    <input type="file" name="csv" accept=".csv" @change="onCsvSelected">
  </div>
  <hr>
  <div class="form-group mt-3">
    <label class="mr-2">Upload Image:</label>
    <input type="file" name="file" @change="onFileSelected">
  </div>
  <hr>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>

            <div v-if="errorMessage"
              class= "alert alert-warning alert-dismissible fade show mt-4"
              role="alert">
                <strong> {{ errorMessage }} </strong>
            </div>

            <div v-if="response_message"
              class= "alert alert-info alert-dismissible fade show mt-4"
              role="alert">
                <strong> {{ response_message }} </strong>
            </div>

</div> 
    </div>
    

</template>

<script>

import NavBar from '@/components/NavBar.vue' // import the Navbar component

export default {
  name: 'AddPost',
  components: {
    NavBar // register the Navbar component as a local component
  },

  data() {
        return {
            errorMessage: "",
            response_message: "",
            title: null,
            description: null,
            imageFile:null,
            csvFile:null,
        };
    },

    methods: {

        onFileSelected(event) {
            console.log(event)
            this.imageFile = event.target.files[0];
            },

            onCsvSelected(event) {
                this.csvFile = event.target.files[0];
              },


        sendNewBlogData(){

            if(this.csvFile){

                if(!this.imageFile ){
                    this.errorMessage = " Kindly also add an image file with csv file"
                  }
                
                else{
                    const formData = new FormData();
                    formData.append('file', this.imageFile);
                    formData.append('csv', this.csvFile);
                    formData.append('csvFlag', "Notnull");
                    
                    const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000//api/BlogData', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => {

                if (response.status === 409){
                  throw new Error("file could not be uploaded");
                }

                else if (response.ok) {
                  this.response_message = "Blog Posted Succesfully"
                  this.errorMessage =""
                  return response.json()
                  }
                })
                // maybe create a time out function here 
            //   .then(() => {
            //     this.$router.push({
            //       name:'MyProfilePage'
            //     })
            //   })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })


                }
                
              }
          

            else if(!this.title || !this.description || !this.imageFile ){
              this.errorMessage = " Kindly add all the required fields"
            }

            
            else{
                
            const formData = new FormData();
            formData.append('file', this.imageFile);
            formData.append('csvFlag', "null");
            formData.append('title', this.title);
            formData.append('description', this.description);
            
            const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000//api/BlogData', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => {

                if (response.status === 409){
                  throw new Error("file could not be uploaded");
                }

                else if (response.ok) {
                  this.response_message = "Blog Posted Succesfully"
                  this.errorMessage =""
                  return response.json()
                  }
                })
                // maybe create a time out function here 
            //   .then(() => {
            //     this.$router.push({
            //       name:'MyProfilePage'
            //     })
            //   })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })

            }
            
        },
    },

}
</script>