window.addEventListener("load", () => {
  console.log("js loaded");
  let dateInput = document.getElementsByName("fecha")[0];
  let date = new Date();

  const year = date.getFullYear().toString();
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");

  const formattedDate = `${year}-${month}-${day}`;

  /* Verifico que la fecha minima sea la actual */
  dateInput.min = formattedDate;
  /* Seteo la fecha actual, para evitar valores nulos al enviar */
  dateInput.value = formattedDate;

  /* Logica que controla el despliegue del campo link inscripcion */
  let select_type = document.getElementsByName("tipo")[0];
  let hidden_field = document.getElementsByClassName("optional-field")[0];
  if (select_type.value === "private") {
    hidden_field.style.visibility = "unset";
  }
  select_type.addEventListener("change", (e) => {
    // console.log({ value: e.target.value });
    if (e.target.value === "private") {
      hidden_field.style.visibility = "unset";
    } else {
      hidden_field.style.visibility = "hidden";
    }
  });

  /* Logica para agregar o quitar input de Datos del Speaker */
  let speaker_row = document.querySelector(".speaker-row");
  let add_btn_speaker = document.getElementById("add-speaker");
  let remove_btn_speaker = document.getElementById("remove-speaker");
  let counter_speaker = 1;

  add_btn_speaker.addEventListener("click", () => {
    counter_speaker++;
    let new_speaker_row = `
      <div class="row speaker-content speaker-${counter_speaker}">
        <div class="mb-3 col-lg-4">
          <label for="imagenSpeaker${counter_speaker}" class="form-label">Imagen Speaker ${counter_speaker}</label>
          <input
            class="form-control"
            type="file"
            name="imagenSpeaker${counter_speaker}"
            accept="image/*"
          />
        </div>
        <div class="mb-3 col-lg-4">
          <label class="form-label" for="nombre${counter_speaker}">Nombre Speaker ${counter_speaker} (*)</label>
          <input
            class="form-control"
            type="text"
            name="nombreSpeaker${counter_speaker}"
            placeholder="Ingrese el nombre del Speaker ${counter_speaker}"
          />
        </div>
        <div class="mb-3 col-lg-4">
          <label class="form-label" for="email${counter_speaker}">Email Speaker ${counter_speaker}</label>
          <input
            class="form-control"
            type="text"
            name="emailSpeaker${counter_speaker}"
            placeholder="Ingrese el email del Speaker ${counter_speaker}"
          />
        </div>
        <div class="mb-3 col-lg-4">
          <label class="form-label" for="linkedin${counter_speaker}">LinkedIn Speaker ${counter_speaker}</label>
          <input
            class="form-control"
            type="text"
            name="linkedinSpeaker${counter_speaker}"
            placeholder="Ingrese el LinkedIn del Speaker ${counter_speaker}"
          />
        </div>
        <div class="mb-3 col-lg-4">
          <label class="form-label" for="cargo${counter_speaker}">Cargo Speaker ${counter_speaker}</label>
          <input
            class="form-control"
            type="text"
            name="cargoSpeaker${counter_speaker}"
            placeholder="Ingrese el cargo del Speaker ${counter_speaker}"
          />
        </div>
        <div class="mb-3 col-lg-4">
          <label class="form-label" for="empresa${counter_speaker}">Empresa Speaker ${counter_speaker}</label>
          <input
            class="form-control"
            type="text"
            name="empresaSpeaker${counter_speaker}"
            placeholder="Ingrese la Empresa del Speaker ${counter_speaker}"
          />
        </div>
      </div>
    `;
    /* se vuelve a llamar por si se agrego informacion */
    speaker_row.appendChild(
      document.createRange().createContextualFragment(new_speaker_row)
    );
    remove_btn_speaker.style.visibility = "unset";
  });

  remove_btn_speaker.addEventListener("click", () => {
    let speakers = document.getElementsByClassName("speaker-content");
    if (speakers.length > 1) {
      if (speakers.length - 1 === 1) {
        remove_btn_speaker.style.visibility = "hidden";
      }

      speakers[speakers.length - 1].remove();
      counter_speaker--;
    }
  });

  /* Logica para agregar o quitar input de Contenido de la Conferencia */
  let content_row = document.getElementsByClassName("content-row")[0];
  let add_btn_content = document.getElementById("add-content");

  add_btn_content.addEventListener("click", () => {
    let content_type = document.querySelector('[name="tipo_contenido"]');
    let contenidos = document.querySelectorAll('[class*="contenido-"]');
    let numerosContenidos = [];

    contenidos.forEach((e) => {
      const match = e.className.match(/\bcontenido-(\d+)\b/);
      if (match) {
        const numero = parseInt(match[1]);
        numerosContenidos.push(numero);
      }
    });

    numerosContenidos.sort((a, b) => a - b);

    let counter_content = null;
    for (let i = 1; i <= numerosContenidos.length; i++) {
      if (!numerosContenidos.includes(i)) {
        counter_content = i;
        break;
      }
    }

    if (counter_content === null) {
      counter_content = numerosContenidos.length + 1;
    }

    let new_content_file = `
      <div class="mb-3 content-item col-lg-4 contenido-${counter_content}">
        <input
          class="form-control"
          type="file"
          name="contenido-${counter_content}"
        />
        <img
          class="add-remove-icon add d-inline-block"
          src="/static/delete.png"
          alt="plus icon"
          id="remove-content-${counter_content}"
          onclick="removeContent(${counter_content})"
        />
      </div>
    `;
    let new_content_url = `
      <div class="mb-3 content-item col-lg-4 contenido-${counter_content}">
        <input
          class="form-control"
          type="text"
          name="contenido-${counter_content}"
          placeholder="Ingrese el url del contenido de la Conferencia"
        />
        <img
          class="add-remove-icon add d-inline-block"
          src="/static/delete.png"
          alt="plus icon"
          id="remove-content-${counter_content}"
          onclick="removeContent(${counter_content})"
        />
      </div>
    `;
    if (content_type.value === "archive") {
      content_row.appendChild(
        document.createRange().createContextualFragment(new_content_file)
      );
    } else if (content_type.value === "link") {
      content_row.appendChild(
        document.createRange().createContextualFragment(new_content_url)
      );
    }
  });

  /* Aqui comienza logica para juntar informacion del speaker
   * y el contenido adjunto en un json
   * para luego enviar el formulario
   */
  let congress_form = document.getElementById("create-congress");
  congress_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    fetch("/edit/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("second then:", data);
        let errorContainer = document.getElementById("error-messages");
        if (data.status !== "200") {
          errorContainer.innerHTML = "";
          data.errors.forEach((error) => {
            console.log({ error });
            let error_text = `<li class="error">${error}</li>`;
            errorContainer.appendChild(
              document.createRange().createContextualFragment(error_text)
            );
          });
        } else {
          errorContainer.innerHTML = "";
          let success_text = `<li class="success">${data.message}</li>`;
          errorContainer.appendChild(
            document.createRange().createContextualFragment(success_text)
          );
          e.target.reset();
        }
        window.scrollTo({ top: 0, behavior: "smooth" });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});

const removeContent = (id) => {
  let content_to_remove = document.getElementsByClassName(`contenido-${id}`)[0];
  content_to_remove.remove();
};
