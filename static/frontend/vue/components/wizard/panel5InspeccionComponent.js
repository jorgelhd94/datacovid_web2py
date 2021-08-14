var inspeccionComponent = { delimiters: [], props: [], data: {}, computed: {}, methods: {} };

inspeccionComponent.delimiters = ["[[", "]]"];

inspeccionComponent.props = ["opcion", "check-opciones", "provincias", "municipios", "datos", "btn-loading"]

inspeccionComponent.data = function () {
    let data = {
        existeNoInspeccion: false,
        existeNoMedidas: false,
        existeNoInspectores: false,
        existeMayorNotificaciones: false,

    };
    return data;
};

inspeccionComponent.mounted = function (){
    this.init();    
}

// Methods
inspeccionComponent.methods = {
    init(){
        $(".custom-select2").select2();
    },
    clase_opcion(opcion) {
        return {
            'current': this.opcion == opcion,
            'disabled': this.opcion != opcion,
            'done': this.checkOpciones[opcion - 1] && this.opcion != opcion
        };
    },
    async finalizar(){
        const isValidMayorNotificaciones = await this.$refs.mayorNotificacionesObserver.validate();

        if (!isValidMayorNotificaciones) {
            // Se activa si ocurre un error en el formulario
            swal("Error!!", "Existen errores en el formulario.", "error");
        }
        else{
            this.$emit('finalizar');
        }
    },
    async incrementarOpcion() {
        const isValidNoInspeccionaron = await this.$refs.noInspeccionaronObserver.validate();
        const isValidNoMedidas = await this.$refs.noMedidasObserver.validate();
        const isValidNoInspectores = await this.$refs.noInspectoresObserver.validate();
        
        let continuar = true;
        const mostrarError = () => {
            swal("Error!!", "Existen errores en el formulario.", "error");
            continuar = false;
        };

        switch (parseInt(this.opcion)) {
            case 17:
                if (!isValidNoInspeccionaron) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 18:
                if (!isValidNoMedidas) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 19:
                if (!isValidNoInspectores) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 20:
                if (!isValidMayorNotificaciones) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;

            default:
                break;
        }

        if (continuar) {
            if (!this.checkOpciones[this.opcion - 1]) {
                this.checkOpciones[this.opcion - 1] = true;
            }
            this.$emit('incrementar-opcion');

        }
    },
    decrementarOpcion() {
        this.$emit('decrementar-opcion')
    },
    addNoInspeccionaron() {
        const id_no_inspeccionaron = document.querySelector("#selectNoInspeccionaron").value;

        const existe_no_inspeccionaron = this.datos.inspeccion_sanitaria_estatal.municipio_no_salieron.find((value) => {
            return value.id == id_no_inspeccionaron;
        });

        if (!existe_no_inspeccionaron) {
            this.existeNoInspeccion = false;
            const municipio = this.municipios.find((value) => {
                return value.id == id_no_inspeccionaron;
            });

            this.datos.inspeccion_sanitaria_estatal.municipio_no_salieron.push({
                id: municipio.id,
                nombre: municipio.nombre,
            });
        }
        else {
            this.existeNoInspeccion = true;
        }
    },
    quitarNoInspeccionaron(key) {
        this.datos.inspeccion_sanitaria_estatal.municipio_no_salieron.splice(key, 1);
    },
    addNoMedidas() {
        const id_no_medidas = document.querySelector("#selectNoMedidas").value;

        const existe_no_medidas = this.datos.inspeccion_sanitaria_estatal.municipio_no_medidas.find((value) => {
            return value.id == id_no_medidas;
        });

        if (!existe_no_medidas) {
            this.existeNoMedidas = false;
            const municipio = this.municipios.find((value) => {
                return value.id == id_no_medidas;
            });

            this.datos.inspeccion_sanitaria_estatal.municipio_no_medidas.push({
                id: municipio.id,
                nombre: municipio.nombre,
                
            });
        }
        else {
            this.existeNoMedidas = true;
        }
    },
    quitarNoMedidas(key) {
        this.datos.inspeccion_sanitaria_estatal.municipio_no_medidas.splice(key, 1);
    },
    addNoInspectores() {
        const id_no_inspectores = document.querySelector("#selectNoInspectores").value;

        const existe_no_inspectores = this.datos.inspeccion_sanitaria_estatal.municipio_no_inspectores.find((value) => {
            return value.id == id_no_inspectores;
        });

        if (!existe_no_inspectores) {
            this.existeNoInspectores = false;
            const municipio = this.municipios.find((value) => {
                return value.id == id_no_inspectores;
            });

            this.datos.inspeccion_sanitaria_estatal.municipio_no_inspectores.push({
                id: municipio.id,
                nombre: municipio.nombre,
                
            });
        }
        else {
            this.existeNoInspectores = true;
        }
    },
    quitarNoInspectores(key) {
        this.datos.inspeccion_sanitaria_estatal.municipio_no_inspectores.splice(key, 1);
    },
    addMayorNotificaciones() {
        const id_mayor_notificaciones = document.querySelector("#selectMayorNotificaciones").value;

        const existe_mayor_notificaciones = this.datos.inspeccion_sanitaria_estatal.municipio_mayor_notificaciones.find((value) => {
            return value.id == id_mayor_notificaciones;
        });

        if (!existe_mayor_notificaciones) {
            this.existeMayorNotificaciones = false;
            const municipio = this.municipios.find((value) => {
                return value.id == id_mayor_notificaciones;
            });

            this.datos.inspeccion_sanitaria_estatal.municipio_mayor_notificaciones.push({
                id: municipio.id,
                nombre: municipio.nombre,
                
            });
        }
        else {
            this.existeMayorNotificaciones = true;
        }
    },
    quitarMayorNotificaciones(key) {
        this.datos.inspeccion_sanitaria_estatal.municipio_mayor_notificaciones.splice(key, 1);
    },
};


// Register Component
utils.register_vue_component('inspeccion', url_inspeccionComponent, function (template) {
    inspeccionComponent.template = template.data;
    return inspeccionComponent;
});