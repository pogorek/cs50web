document.addEventListener("DOMContentLoaded", function () {
	load_user();
});

const postBox = document.getElementById("post-box");
const userBox = document.getElementById("user-box");
const followBox = document.getElementById("follow-box");

followBox.innerHTML = '<button href="#" class="btn btn-primary" id="follow-box>';

const url = window.location.href + "user_page/";
const urlUser = window.location.href;
var user_id = urlUser.slice(32);

if (urlUser.slice(32, urlUser.indexOf("#")) == "") {
	user_id = urlUser.slice(32);
} else {
	user_id = urlUser.slice(32, urlUser.indexOf("#"));
}

const load_user = (current_page = 1) => {
	fetch(`/user_page_data/${user_id}/${current_page}`)
		.then((response) => response.json())
		.then((data) => {
			// Print email
			console.log(data);

			let following = data.user.follow.includes(data.user_id);

			if (data.visitor) {
				followBox_html = `<form id="follow-forms" data-follow-id="${data.user.id}">
				<button href="#" class="btn btn-primary" id="follow-${data.user.id}">${following ? `Unfollow` : `Follow`}</button>
			</form>`;
			} else {
				followBox_html = "";
			}

			// user section
			userBox.innerHTML = `
				<h3 class="mt-2">${data.user.username}'s Page${followBox_html}</h3>
				<div>Followers - <b>${data.user.followers}</b></div>
				<div>Following - <b>${data.user.following}</b></div>
				<hr>
				<h4 class="ms-2">User posts</h4>
				`;

			// add follow button and listener
			followUser();
			// user posts section
			postBox.innerHTML = "";
			data.p_data.pages.forEach((el) => {
				postBox.innerHTML += `
		<div class="card mb-2" id="edit-card-${el.id}">
			<div class="card-body"
				<h5 class="card-title">Post ${el.id}</h5>
				<p class="card-text" id="edit-content-${el.id}">${el.content}</p>
				<span class="text-muted">Author:
				<a href="${urlUser}"><b>${el.author}</b></a></span><br>
				<span class="text-muted">${el.time_created}</span>
			</div>
			<div class="card-footer">
				<div class="row">
				${
					!data.visitor
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
			console.log("in load page :", data);
			const pagBox = document.getElementById("pag-box");
			let pagBody = "";
			for (let i = 1; i <= data.p_data.num_pages; i++) {
				pagBody += `<li class="page-item ${data.p_data.current_page == i ? "active" : ""}">
		<a class="page-link ${data.p_data.current_page == i ? "disabled" : ""}" href="#" data-pag-id="${i}">${i}</a>
	</li>`;
				console.log("in pagination: ", i);
			}
			pagBox.innerHTML = `
	<nav aria-label="...">
                <ul class="pagination">
                    <li class="page-item ${!data.p_data.previous ? "disabled" : ""}">
                        <a class="page-link" href="#" data-pag-id="${data.p_data.current_page == 1 ? 1 : data.p_data.current_page - 1}">Previous</a>
                    </li>
                    ${pagBody}
                    <li class="page-item ${!data.p_data.next ? "disabled" : ""}">
                        <a class="page-link " href="#" data-pag-id="${data.p_data.current_page == data.p_data.num_pages ? data.p_data.num_pages : data.p_data.current_page + 1}">Next</a>
                    </li>
                </ul>
            </nav>
			`;

			const pageLinks = [...document.getElementsByClassName("page-link")];
			console.log("bef pageLinks", pageLinks);
			pageLinks.forEach((el) =>
				el.addEventListener("click", (e) => {
					console.log("in page item for each");
					const clickedId = e.target.getAttribute("data-pag-id");
					console.log("clickedId: ", clickedId);
					load_user(clickedId);
				})
			);
			likeUnlikePosts();
			editPosts();
		});
};

// Follow section
const followUser = () => {
	// transform elements to array with spread operator
	const followForm = document.getElementById("follow-forms");
	console.log(followForm);
	if (followForm == null) {
		return;
	}

	// listen for submit
	followForm.addEventListener("submit", (e) => {
		// we dont want form to submit, we want to create our own logic - send data with ajax
		e.preventDefault();
		// get id from "data-" id of the form that has been clicked/submitted
		const clickedId = e.target.getAttribute("data-follow-id");

		// alert("FOLLOW CLOCK");

		fetch("/follow_user/", {
			method: "POST",
			body: JSON.stringify({
				pk: clickedId,
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				// Print email
				load_user();
				console.log(result.result);
			})
			.catch((error) => {
				console.log(error);
			});
	});
};
