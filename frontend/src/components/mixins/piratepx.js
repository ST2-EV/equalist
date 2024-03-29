import {options} from "../../assets/backend-url"
export default {
    methods: {
        addToAnalytics(id) {
            if (options.analytics){
                const query = new URLSearchParams({
                    p: '62b908a8-3335-48c0-8044-38f7b88d136b',
                    i: id,
                  })
                fetch(`https://app.piratepx.com/ship?${query.toString()}`)
            } 
        }
    }
}