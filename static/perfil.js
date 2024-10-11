window.addEventListener("load", () => {
  let profile_form = document.getElementById("edit-profile");
  profile_form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    fetch("/profile/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "200") {
          e.target.reset();
        }
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
