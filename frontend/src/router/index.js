import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store"

const routes = [
    {
        path: '/',
        name: 'UsersList',
        component: () => import('@/views/UsersList.vue'),
        meta: {
            // load page data before displaying the page
            loadData(to, from, next) {
                return new Promise(resolve => {
                    Promise.all([
                        // get users list
                        store.dispatch('usersList', to.query.path),
                        // get roles list
                        store.dispatch('rolesList')
                    ]).then(() => {
                        // if not path in query, then set path=users
                        if (!to.query.path) {
                            next({
                                path: '/',
                                query: {
                                    path: 'users'
                                }
                            })
                        } else {
                            next()
                        }
                        resolve()
                    })
                })
            }
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.loadData) {
        // await load page data, next using in load data
        to.meta.loadData(to, from, next)
    } else {
        next()
    }
})

export default router
