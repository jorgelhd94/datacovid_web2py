var casosComponent = { delimiters: [], props: [], data: {}, computed: {}, methods: {} };

casosComponent.delimiters = ["[[", "]]"];

casosComponent.props = ["opcion", "check-opciones", "provincias", "municipios",
    "municipios_ubicaciones", "ubicaciones", "grupo_edades", "datos"]

casosComponent.data = function () {
    let data = {
        // Mensajes de error
        existeMunicipio: false,
        existeGrupoEdades: false,
        existeUbicacion: false,

    };
    return data;
};

casosComponent.mounted = function () {
    this.init();
}

// Computed
casosComponent.computed = {
    // Confirmados
    error_sint_asin() {
        const total = parseInt(this.datos.confirmados.sintomaticos) + parseInt(this.datos.confirmados.asintomaticos);
        if (total !== parseInt(this.datos.confirmados.total)) {
            return true;
        }

        return false;
    },
    error_cub_ext() {
        const total = parseInt(this.datos.confirmados.cubanos) + parseInt(this.datos.confirmados.extranjeros);
        if (total !== parseInt(this.datos.confirmados.total)) {
            return true;
        }

        return false;
    },
    error_masc_fem() {
        const total = parseInt(this.datos.confirmados.masculinos) + parseInt(this.datos.confirmados.femeninos);
        if (total !== parseInt(this.datos.confirmados.total)) {
            return true;
        }

        return false;
    },
    // Municipios
    error_municipios() {
        let total = 0;
        this.datos.confirmados.municipios.forEach(element => {
            total += parseInt(element.cantidad);
        });

        if (total !== parseInt(this.datos.confirmados.total)) {
            return true;
        }

        return false;
    },
    // Grupo de edades
    error_grupo_edades() {
        let total = 0;
        this.datos.confirmados.grupo_edades.forEach(element => {
            total += parseInt(element.cantidad);
        });

        if (total !== parseInt(this.datos.confirmados.total)) {
            return true;
        }

        return false;
    },
    // Activos - Ubicacion
    error_ubicacion_activos() {
        let total = 0;
        this.datos.activos.ubicaciones.forEach(element => {
            total += parseInt(element.cantidad);
        });

        if (total !== parseInt(this.datos.activos.total)) {
            return true;
        }

        return false;
    },
};

// Methods
casosComponent.methods = {
    init() {
        $(".custom-select2").select2();
    },
    clase_opcion(opcion) {
        return {
            'current': this.opcion == opcion,
            'disabled': this.opcion != opcion,
            'done': this.checkOpciones[opcion - 1] && this.opcion != opcion
        };
    },
    async incrementarOpcion() {
        const isValidConfirmados = await this.$refs.confirmadosObserver.validate();
        const isValidMunicipios = await this.$refs.municipiosObserver.validate();
        const isValidEdades = await this.$refs.edadesObserver.validate();
        const isValidActivos = await this.$refs.activosObserver.validate();

        let continuar = true;
        const mostrarError = () => {
            swal("Error!!", "Existen errores en el formulario.", "error");
            continuar = false;
        };

        switch (parseInt(this.opcion)) {
            case 1:
                if (!isValidConfirmados || this.error_sint_asin || this.error_cub_ext || this.error_masc_fem) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 2:
                if (!isValidMunicipios || this.error_municipios) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 3:
                if (!isValidEdades || this.error_grupo_edades) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 4:
                if (!isValidActivos || this.error_ubicacion_activos) {
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
    addMunicipio() {
        const id_municipio = document.querySelector("#selectMunicipio").value;

        const existe_municipio = this.datos.confirmados.municipios.find((value) => {
            return value.id == id_municipio;
        });

        if (!existe_municipio) {
            this.existeMunicipio = false;
            const municipio = this.municipios.find((value) => {
                return value.id == id_municipio;
            });

            this.datos.confirmados.municipios.push({
                id: municipio.id,
                nombre: municipio.nombre,
                cantidad: 0,
            });
        }
        else {
            this.existeMunicipio = true;
        }
    },
    quitarMunicipio(key) {
        this.datos.confirmados.municipios.splice(key, 1);
    },
    addGrupoEdades() {
        const id_grupo_edades = document.querySelector("#selectGrupoEdades").value;

        const existe_grupo_edades = this.datos.confirmados.grupo_edades.find((value) => {
            return value.id == id_grupo_edades;
        });

        if (!existe_grupo_edades) {
            this.existeGrupoEdades = false;

            const edades = this.grupo_edades.find((value) => {
                return value.id == id_grupo_edades;
            });

            this.datos.confirmados.grupo_edades.push({
                id: edades.id,
                grupo: edades.grupo,
                cantidad: 0,
            });
        }
        else {
            this.existeGrupoEdades = true;
        }
    },
    quitarGrupoEdades(key) {
        this.datos.confirmados.grupo_edades.splice(key, 1);
    },
    addUbicacion() {
        const id_ubicacion = document.querySelector("#selectUbicacion").value;

        if (id_ubicacion !== "0") {

            const existe_ubicacion = this.datos.activos.ubicaciones.find((value) => {
                return value.id == id_ubicacion;
            });

            if (!existe_ubicacion) {
                this.existeUbicacion = false;

                const ubicacion = this.ubicaciones.find((value) => {
                    return value.id == id_ubicacion;
                });

                this.datos.activos.ubicaciones.push({
                    id: ubicacion.id,
                    nombre: ubicacion.nombre,
                    cantidad: 0,
                });
            }
            else {
                this.existeUbicacion = true;
            }
        }
    },
    quitarUbicacion(key) {
        this.datos.activos.ubicaciones.splice(key, 1);
    }
};


// Register Component
utils.register_vue_component('casos', url_casosComponent, function (template) {
    casosComponent.template = template.data;
    return casosComponent;
});