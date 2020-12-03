<template>
    <div class="main">
        <div class="container">
            <div class="nav_parrents">
                <div class="inner" v-for="(role, i) in roleParents" :key="'roleParrent' + role.id">
                    <router-link :to="'/?path=' + role.path">{{ role.name  }}</router-link>
                    <div v-if="i + 1 < roleParents.length" class="decor"> > </div>
                </div>
            </div>
            <div class="nav_childs">
                <router-link v-for="role in roleChilds" :to="'/?path=' + role.path" :key="'roleChild' + role.id">{{ role.name }}</router-link>
            </div>

            <div class="users_list">
                <div class="head">Список пользователей</div>
                <div class="user" v-for="(user, i) in $store.getters.usersList" :key="'user' + user.id">
                    <div class="user_data">
                        <div class="username">{{ user.username }}</div>
                        <div class="role">{{ user.role }}</div>
                    </div>
                    <div v-if="i + 1 < $store.getters.usersList.length" class="decor"></div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    computed: {
        // get role parents list
        roleParents() {
            let parents
            // if path in request query
            if (this.$route.query.path && this.$route.query.path != '') {
                // get roles
                parents = this.$store.getters.rolesList.filter(r => this.$route.query.path.indexOf(r.path) == 0)
            } else {
                parents = []
            }
            return parents
        },
        // get role childs list
        roleChilds() {
            let childs
            if (this.$route.query.path && this.$route.query.path != '') {
                childs = this.$store.getters.rolesList.filter(r => (
                    r.path.indexOf(this.$route.query.path) == 0
                    && r.path.split('.').length - 1 == this.$route.query.path.split('.').length
                ))
            } else {
                childs = this.$store.getters.rolesList.filter(r => r.path.split('.').length == 2)
            }
            return childs
        }
    }
}
</script>


<style lang="scss" scoped>
$dark: #2C3E4E;
$green: #009166;
.main {
    display: flex;
    justify-content: center;
    background: #F9F9F9;
    .container {
        background: #FFFFFF;
        width: 100%;
        min-height: 100vh;
        max-width: 600px;
        box-sizing: border-box;
        padding: 20px;
        .nav_parrents {
            display: flex;
            margin-bottom: 20px;
            .inner {
                display: flex;
                align-items: center;
                .decor {
                    margin: 0 10px;
                    font-size: 12px;
                }
                a {
                    font-size: 15px;
                    font-weight: 700;
                    text-transform: uppercase;
                    text-decoration: none;
                    color: $dark;
                }
            }
        }
        .nav_childs {
            margin-bottom: 40px;
            display: flex;
            flex-direction: column;
            a {
                font-size: 14px;
                font-weight: 700;
                text-transform: uppercase;
                text-decoration: none;
                color: $green;
                margin-bottom: 5px;
            }
        }
        .users_list {
            .head {
                font-size: 18px;
                margin-bottom: 25px;
                position: relative;
                display: inline-block;
            }
            .head::after {
                content: "";
                position: absolute;
                left: 0;
                top: 100%;
                width: 100%;
                height: 2px;
                background: $green;
            }
            .user {
                .user_data {
                    display: flex;
                    .username {
                        width: 400px;
                    }
                }
                .decor {
                    width: 100%;
                    height: 1px;
                    background: #E7E8EC;
                    margin: 10px 0;
                }
            }
        }
    }
}
</style>
