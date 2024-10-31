// ************ CUSTOM METHODS START ************
// Methods for "marking item watched and unwatched". Will be reused by multiple event listeners. DRY.

// Accepts a string which is a movie id
async function mark_watched(id) {
    // Sending a patch request using axios and passing the movie id and the W as the oper
    res = await axios.patch("/watched_unwatched", {
        mov_id: id,
        oper: 'w'
    })
}

// Accepts a string which is a movie id
async function mark_unwatched(id) {
    // Sending a patch request using axios and passing the movie id and the U as the oper
    res = await axios.patch("/watched_unwatched", {
        mov_id: id,
        oper: 'u'
    })
}

// Accepts a string which is a movie id and plist_id
// Methods for "adding item to playlist". Will be reused by multiple event listeners. DRY.
async function add_to_playlist(mov_id, plist_id) {
    // Sending a patch request using axios and passing the data sent to this method
    res = await axios.patch("/playlist/add_remove", {
        mov_id: mov_id,
        plist_id: plist_id
    })
}

// Accepts a string which is a movie id and plist_id
async function remove_from_playlist(mov_id, plist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/playlist/add_remove", {
        data: {
            mov_id: mov_id,
            plist_id: plist_id
        }
    })

}

// Accepts a string which is a playlist id
// Methods for removing and sharing private playlists. Will be reused by multiple event listeners. DRY.
async function delete_playlist(plist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/playlist/delete", {
        data: {
            plist_id: plist_id
        }
    })
}

// Accepts a string which is a playlist id
async function share_playlist(plist_id) {
    // Sending a put request using axios and passing the data sent to this method
    res = await axios.put("/playlist/share", {
        plist_id: plist_id
    })
    // Return the result of the PUT request which is the URL generated on the back-end in a string format
    return res.data;
}

// Accepts a string which is a playlist id
async function unshare_playlist(plist_id) {
    // Sending a delete request using axios and passing the data sent to this method
    res = await axios.delete("/playlist/shared", {
        data: {
            plist_id: plist_id
        }
    })
}

// ************ CUSTOM METHODS END ************

// MOVIE DETAILS > WATCH / UNWATCH BUTTON EVENT LISTENER
// All the MOVIE DETAILS methods are wrappen in the if statement to make sure it only runs on the right page
if (window.location.href.indexOf("movie/") > -1 && window.location.href.indexOf("/images") === -1) {
    // mapping the DOM element to a variable
    btn_watch_unwatch = document.getElementById('btn_watch_unwatch')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (btn_watch_unwatch !== null) {
        // adding on event listener for click
        btn_watch_unwatch.addEventListener('click', function (e) {
            // preventing the default behavior of the DOM element
            e.preventDefault()
            // if the button shows as watched
            if (btn_watch_unwatch.innerText === " Mark as watched") {
                // mapping the DOM element to a variable
                movie_id = document.getElementById('movie_id').innerText
                // Marking the movie as watched
                mark_watched(movie_id)
                // Setting the inner html of the button to an updated icon and text
                btn_watch_unwatch.innerHTML = '<i class="bi bi-bookmark-dash-fill"></i> Mark not watched'
                //if the button shows not watched, do this
            } else if (btn_watch_unwatch.innerText === " Mark not watched") {
                // mapping the DOM element to a variable
                movie_id = document.getElementById('movie_id').innerText
                // Marking the movie as watched
                mark_unwatched(movie_id)
                // Setting the inner html of the button to an updated icon and text
                btn_watch_unwatch.innerHTML = '<i class="bi bi-bookmark-plus"></i></i> Mark as watched</button>'
            } else {
                // If there is an issue, showing a message in the console.
                console.log('Error. Could not mark the movie as watched/unwatched.')
            }
        })
    }

    // MOVIE DETAILS > POSTER HOVER LOGIC TO SHOW MORE IMAGES
    // mapping the DOM elements to a variables
    movie_details_poster_div = document.getElementById('movie-details-poster-div')
    movie_details_poster_text = document.getElementById('movie-details-poster-txt-div')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (movie_details_poster_text !== null && movie_details_poster_div !== null) {
        // adding on event listener for hovering
        movie_details_poster_div.addEventListener('mouseover', function (e) {
            // preventing the default behavior of the DOM element
            e.preventDefault()
            // setting the css visibility of the element
            movie_details_poster_text.style.setProperty('visibility', 'visible')
        })
        // adding on event listener for hovering
        movie_details_poster_div.addEventListener('mouseout', function (e) {
            // preventing the default behavior of the DOM element
            e.preventDefault()
            // setting the css visibility of the element
            movie_details_poster_text.style.setProperty('visibility', 'hidden')
        })
    }

    // MOVIE DETAILS > ADD TO PLAYLIST LOGIC
    // Will only work if we are on the right page
    // mapping the DOM element to a variable
    movie_detail_playlist_item = document.querySelectorAll("#movie-detail-playlist-item")
    // mapping the DOM element to a variable
    movie_id = document.getElementById('movie_id').innerText
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (movie_detail_playlist_item !== null && movie_id !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of movie_detail_playlist_item) {
            // If there is a p in the div saying that the movie already exists in the playlist, do this
            if (i.children[1]) {
                // Setting the background color of the div as green
                i.style.setProperty('background-color', 'limegreen')
                // If the movie is not in the playlist yet, do this
            } else {
                // adding on event listener for clicking
                i.addEventListener('click', function (e) {
                    // preventing the default behavior of the DOM element
                    e.preventDefault()
                    // getting the id attibute which stored the id of the playlist on the Jinja side
                    playlist_id = i.parentElement.getAttribute('id')
                    // calling the custom method
                    add_to_playlist(movie_id, playlist_id)
                    // updating the inner HTML
                    i.innerHTML = '<h5 class="mb-0"><i class="bi bi-check2"></i> Added to playlist</h5>'
                    // making the div green
                    i.style.setProperty('background-color', 'limegreen')
                })
            }
        }
    }
}

// PLAYLIST > WATCHED > REMOVE BUTTON EVENT LISTENER
if (window.location.href.indexOf("playlist/watched") > -1) {
    // mapping the DOM element to a variable
    btn_playlist_watched_remove = document.querySelectorAll('#playlist-watched-remove-button')
    // only running this logic if we are on the correct page (if we get a result from our queryselectorall)
    if (btn_playlist_watched_remove !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of btn_playlist_watched_remove) {
            // adding on event listener for clicking
            i.addEventListener('click', function (e) {
                // preventing the default behavior of the DOM element
                e.preventDefault()
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === '<i class="bi bi-trash3"></i> Remove') {
                    i.innerHTML = "Are you sure?"

                    // If the button does not say that, do the following. Example is second click after Are you sure?. 
                } else {
                    // getting the id attribute of the parent which is a movie id
                    movie_id = i.parentElement.getAttribute('id')
                    // calling the custom method and passing the movie id
                    mark_unwatched(movie_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }
}

// PLAYLIST > PRIVATE > LIST OF PRIVATE PLAYLISTS
// REMOVE BUTTON EVENT LISTENER
if (window.location.href.indexOf("playlist/private") > -1) {
    // mapping the DOM element to a variable
    playlist_private_remove_button = document.querySelectorAll('#playlist-private-remove-button')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (playlist_private_remove_button !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of playlist_private_remove_button) {
            // adding on event listener for clicking
            i.addEventListener('click', function (e) {
                // preventing the default behavior of the DOM element
                e.preventDefault()
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === '<i class="bi bi-trash3"></i> Remove') {
                    i.innerHTML = "Are you sure?"

                    // If the button does not say that, do the following. Example is second click after Are you sure?. 
                } else {
                    // getting the id attribute of the parent which is a playlist id
                    playlist_id = i.parentElement.getAttribute('id')
                    // calling the custom method and passing the playlist id
                    delete_playlist(playlist_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }

    // SHARE  BUTTON EVENT LISTENER
    // mapping the DOM element to a variable
    playlist_private_share_button = document.querySelectorAll('#playlist-private-share-button')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (playlist_private_share_button !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of playlist_private_share_button) {
            // adding on event listener for clicking
            i.addEventListener('click', function (e) {
                // preventing the default behavior of the DOM element
                e.preventDefault()
                playlist_id = i.parentElement.getAttribute('id')

                if (i.getAttribute('url')) {
                    // if the playlist already has a shared url, don't send axios reqest, just redirect
                    // prevents us from causing DB collision issues. We don't want to generate URLs multiple times
                    let url = i.getAttribute('url')
                    // redirecting the user to the shared url page
                    location.href = `/playlist/shared/${url}`;
                } else {
                    // if the playlist does not have a url yet, send an axios PUT request
                    // then store the PROMISE into a variable
                    let u = share_playlist(playlist_id)
                    // resolve the promise into a response (which is a URL)
                    // then redirect the user into a newly shared playlist
                    u.then(data => { location.href = `/playlist/shared/${data}`; })
                }
            })
        }
    }

    // PLAYLIST > PRIVATE > OPEN SINGLE PLAYLIST DETAILS
    // mapping the DOM element to a variable
    playlist_private_details_remove_button = document.querySelectorAll('#playlist-private-details-remove-button')
    // only running this logic if we are on the correct page (if we get a result from our queryselectorall)
    if (playlist_private_details_remove_button !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of playlist_private_details_remove_button) {
            // adding on event listener for clicking
            i.addEventListener('click', function (e) {
                // preventing the default behavior of the DOM element
                e.preventDefault()
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === '<i class="bi bi-trash3"></i> Remove') {
                    i.innerHTML = "Are you sure?"

                    // If the button does not say that, do the following. Example is second click after Are you sure?. 
                } else {
                    // getting the id attribute of the parent which is a movie id
                    movie_id = i.parentElement.getAttribute('mov_id')
                    plist_id = i.parentElement.getAttribute('plist_id')
                    // calling the custom method and passing the movie id and playlist id
                    remove_from_playlist(movie_id, plist_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }
            })
        }
    }
}

// PLAYLIST > SHARED > LIST OF PRIVATE PLAYLISTS
if (window.location.href.indexOf("playlist/shared") > -1) {
    // UN-SHARE BUTTON EVENT LISTENER
    // mapping the DOM element to a variable
    playlist_shared_unshare_button = document.querySelectorAll('#playlist-shared-unshare-button')
    // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
    if (playlist_shared_unshare_button !== null) {
        // since the querySelectAll returns a list, running the following for each item
        for (let i of playlist_shared_unshare_button) {
            // adding on event listener for clicking
            i.addEventListener('click', function (e) {
                // preventing the default behavior of the DOM element
                e.preventDefault()
                plist_id = i.parentElement.getAttribute('id')
                // if the button says Remove, make sure we display Are you sure to confirm
                if (i.innerHTML === '<i class="bi bi-person-x"></i> Un-share') {
                    i.innerHTML = "Are you sure?"

                    // If the button does not say that, do the following. Example is second click after Are you sure?. 
                } else {
                    // calling the custom method and passing the playlist id
                    unshare_playlist(plist_id)
                    // removing the div that we clicked on
                    i.parentElement.parentElement.parentElement.remove()
                }

            })
        }

        // COPY URL BUTTON EVENT LISTENER
        // mapping the DOM element to a variable
        playlist_shared_copy_url_button = document.querySelectorAll('#playlist-shared-copy-url-button')
        // only running this logic if we are on the correct page (if we get a result from our getelementbyid)
        if (playlist_shared_copy_url_button !== null) {
            // since the querySelectAll returns a list, running the following for each item
            for (let i of playlist_shared_copy_url_button) {
                // adding on event listener for clicking
                i.addEventListener('click', function (e) {
                    // preventing the default behavior of the DOM element
                    e.preventDefault()
                    // getting the attribute url which is the playlist's url
                    plist_url = i.getAttribute('url')
                    // getting the current url
                    curr_url = window.location.href;
                    // adding the current URL to / character and then the URL that was generated by us
                    full_url = curr_url + '/' + plist_url;

                    // copying the newly created URL into clipboard
                    navigator.clipboard.writeText(full_url);

                    // Setting the inner html and classes to different values to show success
                    i.innerHTML = '<i class="bi bi-clipboard2-check"></i>  Copied'
                    // removing the class of btn-info which provided a blue background
                    i.classList.remove('btn-info')
                    // adding the class of success which makes the background green
                    i.classList.add('btn-success')

                    // Timer for adding the original info and class back
                    setTimeout(() => {
                        i.innerHTML = '<i class="bi bi-clipboard2"></i>  Copy URL'
                        i.classList.remove('btn-success')
                        i.classList.add('btn-info')
                    }, 1500) // 1.5 second timeout.
                })
            }
        }
    }
}

// SEARCH LOGIC
// mapping the DOM element to a variable
search_form = document.getElementById('search-form')
// Adding on event listener for submitting a form. The button type is also submit which triggering the form submission. Thus we don't need an even listener for the search button. Enter or Pressing the button will trigger the search
search_form.addEventListener('submit', function (e) {
    // preventing the default behavior of the DOM element
    e.preventDefault()
    // Finding the search textbox
    // mapping the DOM element to a variable
    search_form_input = document.getElementById('search-form-input');
    console.log("SEARCH_FORM_INPUT >>> ", search_form_input.value);

    if (search_form_input.value === ' ') { (alert("The search query is empty or contains an unsupported character, please try a different search keyword.")) }

    let cleanSearchQuery = Array.from(search_form_input).filter(char => char !== '.' && char !== '/' && char !== '%' && char !== '\\' && char !== '?').join('')
    console.log("CLEANED SEARCH QUERY >>> ", search_form_input);

    // Redirecting the user to the search page
    location.href = `/search/${cleanSearchQuery}/1`;
})
