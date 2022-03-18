document.addEventListener("DOMContentLoaded", function () {
	//document.querySelector("form").onsubmit = compose_submit;

	postNew.addEventListener("submit", function (event) {
		compose_submit(event);
	});
	load_posts();
});

const postNew = document.getElementById("post-new");
const postBox = document.getElementById("post-box");

// var for url - detail page
const urlUser = window.location.href + "user_page/";

// After click SUBMIT - new post
function compose_submit(event) {
	// dont submit - use js
	event.preventDefault();

	// Get form values
	const new_post_textarea = document.querySelector("#new_post_textarea");

	// POST new_post
	fetch("/new_post/", {
		method: "POST",
		body: JSON.stringify({
			new_post_textarea: new_post_textarea.value,
		}),
	})
		.then((response) => {
			console.log("post added", response);
			postBox.innerHTML = "";
			new_post_textarea.value = "";
			load_posts();
		})
		.catch((error) => {
			console.log(error);
		});
}

// Get posts to index postBox
const load_posts = (current_page = 1) => {
	console.log("CP: ", current_page);

	fetch(`/data/${current_page}`)
		.then((response) => response.json())
		.then((post) => {
			postBox.innerHTML = "";
			// Print email
			//console.log("posts: ", post);
			// loading posts
			post.p_data.pages.forEach((el) => {
				postBox.innerHTML += `
			<div class="card mb-2" id="edit-card-${el.id}">
				<div class="card-body">
					<h5 class="card-title">Post ${el.id}</h5>
					<p class="card-text" id="edit-content-${el.id}">${el.content}</p>
					<span class="text-muted">Author: 
					<a href="${urlUser}${el.author_id}"><b>${el.author}</b></a></span><br>
					<span class="text-muted">${el.time_created}</span>
				</div>
				<div class="card-footer">
					<div class="row">
						${
							el.author_id == el.user
								? `
						<div class="col-2">
						<a href="#" class="btn btn-primary edit-post" data-edit-id="${el.id}" id="edit-${el.id}">Edit</a>
						</div>
						`
								: ""
						}
						<div class="col-2">
							<form class="like-unlike-forms" data-form-id="${el.id}">
								<button href="#" class="btn btn-primary" id="like-unlike-${el.id}">${el.liked ? `Unlike (${el.count})` : `Like (${el.count})`}</button>
							</form>
						</div>
					</div>
				</div>
			</div>
							`;
			});
			// pagination
			console.log("in load page :", post);
			const pagBox = document.getElementById("pag-box");
			let pagBody = "";
			for (let i = 1; i <= post.p_data.num_pages; i++) {
				pagBody += `<li class="page-item ${post.p_data.current_page == i ? "active" : ""}">
		<a class="page-link ${post.p_data.current_page == i ? "disabled" : ""}" href="#" data-pag-id="${i}">${i}</a>
	</li>`;
			}
			pagBox.innerHTML = `
	<nav aria-label="...">
                <ul class="pagination">
                    <li class="page-item ${!post.p_data.previous ? "disabled" : ""}">
                        <a class="page-link" href="#" data-pag-id="${post.p_data.current_page == 1 ? 1 : post.p_data.current_page - 1}">Previous</a>
                    </li>
                    ${pagBody}
                    <li class="page-item ${!post.p_data.next ? "disabled" : ""}">
                        <a class="page-link " href="#" data-pag-id="${post.p_data.current_page == post.p_data.num_pages ? post.p_data.num_pages : post.p_data.current_page + 1}">Next</a>
                    </li>
                </ul>
            </nav>
			`;
			const pageLinks = [...document.getElementsByClassName("page-link")];
			pageLinks.forEach((el) =>
				el.addEventListener("click", (e) => {
					console.log("in page item for each");
					const clickedId = e.target.getAttribute("data-pag-id");
					console.log("clickedId: ", clickedId);
					load_posts(clickedId);
				})
			);

			likeUnlikePosts();
			editPosts();
		});
};
