// function to like button - like/unlike

const likeUnlikePosts = () => {
	// transform elements to array with spread operator
	const likeUnlikeForms = [...document.getElementsByClassName("like-unlike-forms")];
	// listen for submit of each form
	likeUnlikeForms.forEach((form) =>
		form.addEventListener("submit", (e) => {
			// we dont want form to submit, we want to create our own logic - send data with ajax
			e.preventDefault();
			// get id from "data-" id of the form that has been clicked/submitted
			const clickedId = e.target.getAttribute("data-form-id");
			// get button element that has been clicked
			const clickedBtn = document.getElementById(`like-unlike-${clickedId}`);

			fetch("/like_unlike/", {
				method: "POST",
				body: JSON.stringify({
					pk: clickedId,
				}),
			})
				.then((response) => response.json())
				.then((result) => {
					// Print email
					clickedBtn.textContent = result.liked ? `Unlike (${result.count})` : `Like (${result.count})`;
					console.log(result);
				})
				.catch((error) => {
					console.log(error);
				});
		})
	);
};

const editPosts = () => {
	// transform elements to array with spread operator
	const editForms = [...document.getElementsByClassName("edit-post")];
	// listen for submit of each form
	editForms.forEach((form) =>
		form.addEventListener("click", (e) => {
			console.log("in edit");
			// we dont want form to submit, we want to create our own logic - send data with ajax
			e.preventDefault();
			// get id from "data-" id of the form that has been clicked/submitted
			const clickedId = e.target.getAttribute("data-edit-id");

			// get  element that has been clicked
			const post = document.getElementById(`edit-content-${clickedId}`);
			const post_content = post.innerHTML;
			const post_card = document.getElementById(`edit-card-${clickedId}`);

			console.log(post_content);
			post_card.innerHTML = `
			<div class="card mb-2" id="edit-card-${clickedId}">
				<div class="card-body">
				<h5 class="card-title">Edit post...</h5>
                <textarea class="form-control" id="edit-textarea" rows="3">${post_content}</textarea>
				</div>
				<div class="card-footer">
					<div class="row">
						<div class="col-2">
							<a href="#" class="btn btn-primary save-post" data-save-id="${clickedId}" id="save-post">Save</a>
						</div>
					</div>
				</div>
			</div>
							`;
			savePosts();
		})
	);
};

const savePosts = () => {
	console.log("in save");

	const savePost = document.getElementById("save-post");

	savePost.addEventListener("click", function (e) {
		e.preventDefault();
		const clickedId = savePost.getAttribute("data-save-id");
		const post_card = document.getElementById(`edit-card-${clickedId}`);

		const content = document.getElementById("edit-textarea").value;
		console.log("save", clickedId);
		console.log(content);

		// console.log(post);

		fetch("/save_post/", {
			method: "POST",
			body: JSON.stringify({
				pk: clickedId,
				content: content,
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				// Print email
				console.log(result);
				post_card.innerHTML = `
				<div class="card mb-2" id="edit-card-${result.data.id}">
					<div class="card-body">
						<h5 class="card-title">Post ${clickedId}</h5>
						<p class="card-text" id="edit-content-${result.data.id}">${result.data.content}</p>
						<span class="text-muted">Author: 
						<a href="${urlUser}${result.data.author_id}"><b>${result.data.author}</b></a></span><br>
						<span class="text-muted">${result.data.time_created}</span>
					</div>
					<div class="card-footer">
						<div class="row">
							${
								result.data.author_id == result.data.user
									? `
							<div class="col-2">
							<a href="#" class="btn btn-primary edit-post" data-edit-id="${result.data.id}" id="edit-${result.data.id}">Edit</a>
							</div>
							`
									: ""
							}
							<div class="col-2">
								<form class="like-unlike-forms" data-form-id="${result.data.id}">
									<button href="#" class="btn btn-primary" id="like-unlike-${result.data.id}">${result.data.liked ? `Unlike (${result.data.count})` : `Like (${result.data.count})`}</button>
								</form>
							</div>
						</div>
					</div>
				</div>
								`;
				likeUnlikePosts();
				editPosts();
			})
			.catch((error) => {
				console.log(error);
			});
	});
};

const loadPag = (post) => {
	console.log("in load page :", post);
	const pagBox = document.getElementById("pag-box");
	let pagBody = "";
	for (let i = 1; i <= post.p_data.num_pages; i++) {
		pagBody += `<li class="page-item ${post.p_data.current_page == i ? "active" : ""}">
		<a class="page-link" href="#">${i}</a>
	</li>`;
	}
	pagBox.innerHTML = `
	<nav aria-label="...">
                <ul class="pagination">
                    <li class="page-item ${!post.p_data.previous ? "disabled" : ""}">
                        <a class="page-link">Previous</a>
                    </li>
                    ${pagBody}
                    <li class="page-item">
                        <a class="page-link ${!post.p_data.next ? "disabled" : ""}" href="#">Next</a>
                    </li>
                </ul>
            </nav>
	`;
};
