<template>
    <!-- <div>
        <p>{{ msg }}</p>
        <div>
            <button @click="NavBarData">Send POST Request</button>
        </div>
    </div> -->

    <!-- <nav class="navbar navbar-expand-lg bg-info-subtle navbar bg-primary" data-bs-theme="dark" > -->
        <!-- <nav   class="navbar navbar-expand-lg bg-info-dark navbar bg-info bg-gradient-info-dark" data-bs-theme="dark"> -->
        <nav class="navbar navbar-expand-lg bg-info-subtle" style="background-color: #c5aa6a;">
    
    <div class="container-fluid " >
      <a class="navbar-brand " href="/">Blog Lite</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/feed">FEED</a>
          </li>

          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/AddPost">SHARE A POST</a>
          </li>

          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/MyProfilePage">My Profile</a>
          </li>

          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/"  @click="logout()">Logout</a>
          </li>

          <!-- <li class="nav-item dropdown" >
            <a class="nav-link dropdown-toggle "  href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false" >
              test
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="?">My Profile</a></li>
              <li><a class="dropdown-item" href="#">Another action</a></li>
              
            </ul>
          </li> -->

        </ul>

        <!-- <form class="d-flex" role="search" action="#" method="get" @submit.prevent="searchUsers">
          <input class="form-control me-2" type="search" name="q" placeholder="Search Users" aria-label="Search" v-model="searchQuery">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <ul>
            <li v-for="user in searchResults" :key="user.id">{{ user.username }}</li>
        </ul> -->

        <div class="position-relative">
          <form class="d-flex" role="search" action="#" method="get" @submit.prevent="searchUsers">
            <input class="form-control me-2" type="search" name="q" placeholder="Search Users" aria-label="Search" v-model="searchQuery">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
          <div v-if="searchResults.length > 0 && showSearchResults" class="position-absolute top-100 start-0 mt-1 w-100 dropdown-menu">
            <ul class="list-group">
              <li  v-for="user in searchResults" :key="user.Uid" class="list-group-item">
                <router-link :to="{ name: 'UserProfilePage', params: { username: user.username } }">{{ user.username }}</router-link>
              </li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  </nav>
</template>

<style>
  .btn-custom {
    padding: 4px 8px;
    font-size: 6px;
  }
  .position-relative {
    display: inline-block;
  }

  .dropdown-menu {
  display: block !important;
  position: absolute !important;
  top: 100% !important;
  left: 0 !important;
  z-index: 1000 !important;
  float: none !important;
  min-width: 10rem !important;
  padding: .5rem 0 !important;
  margin: .125rem 0 0 !important;
  font-size: 1rem !important;
  color: #212529 !important;
  text-align: left !important;
  list-style: none !important;
  background-color: #fff !important;
  background-clip: padding-box !important;
  border: 1px solid rgba(0,0,0,.15) !important;
  border-radius: .25rem !important;
}

.form-control:focus + .dropdown-menu {
  display: block !important;
}     

</style>

<script>

export default {
  name: 'NavBar',

  data() {
    return {
      searchQuery: '',
      searchResults: [],
      showSearchResults: false
    }
  },

  methods: {
    async searchUsers() {

      const token = localStorage.getItem('access_token');
      const url = `http://127.0.0.1:5000/api/SearchUsers?q=${this.searchQuery}`;
  const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      const init = {
        method: 'GET',
        headers: headers
      };
      try {
        const response = await fetch(url, init);
        const data = await response.json();
        this.searchResults = data;
      } catch (error) {
        console.error(error);
      }
    },
    //   const response = await fetch(`http://127.0.0.1:5000/api/SearchUsers?q=${this.searchQuery}`)
    //   // const response = await fetch(`http://127.0.0.1:5000/api/SearchUsers/ + searchQuery`)
    //   const data = await response.json()
    //   this.searchResults = data
    // },
      logout() {
        localStorage.removeItem('access_token');
        // redirect the user to the login page
        this.$router.push({
              name: 'Login_Home'
            });
      },
  },
  watch: {
    searchQuery(newValue, oldValue) {
    if (newValue === '') {
      this.showSearchResults = false
      console.log('searchQuery is empty')
    } else {
      this.showSearchResults = true
      console.log('searchQuery is not empty')
    }
    if (newValue !== oldValue) {
      this.searchUsers();
    }
  }
  },
}
</script>



<!-- 
<script>

export default {
    name:'NavBar',
    data() {
        return {
            msg: ""
        };
    },
    methods: {
        NavBarData(){
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
    

    // sendPostRequest() {
    //     console.log('sendPostRequest method called');
    //         const path = 'http://localhost:5000/shark'
    //         axios.post(path)
    //         .then(resp => {
    //             this.msg = resp.data;
    //             console.log('POST request sent successfully');
    //         })
    //         .catch(error => {
    //             console.log(error);
    //         });
    //     },
    },

    created(){
        this.NavBarData()
    }
} 

-->