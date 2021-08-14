//Rules
VeeValidate.extend('required', VeeValidateRules.required);
VeeValidate.extend('min_value', VeeValidateRules.min_value);
VeeValidate.extend('max_value', VeeValidateRules.max_value);
VeeValidate.extend('numeric', VeeValidateRules.numeric);
VeeValidate.extend('regex', VeeValidateRules.regex);



VeeValidate.localize({
    es: {
        messages: {
            "alpha": "El campo {_field_} solo debe contener letras",
            "alpha_dash": "El campo {_field_} solo debe contener letras, n�meros y guiones",
            "alpha_num": "El campo {_field_} solo debe contener letras y n�meros",
            "alpha_spaces": "El campo {_field_} solo debe contener letras y espacios",
            "between": "El campo {_field_} debe estar entre {min} y {max}",
            "confirmed": "El campo {_field_} no coincide",
            "digits": "El campo {_field_} debe ser num�rico y contener exactamente {length} d�gitos",
            "dimensions": "El campo {_field_} debe ser de {width} p�xeles por {height} p�xeles",
            "email": "El campo {_field_} debe ser un correo electr�nico v�lido",
            "excluded": "El campo {_field_} debe ser un valor v�lido",
            "ext": "El campo {_field_} debe ser un archivo v�lido",
            "image": "El campo {_field_} debe ser una imagen",
            "oneOf": "El campo {_field_} debe ser un valor v�lido",
            "integer": "El campo {_field_} debe ser un entero",
            "length": "El largo del campo {_field_} debe ser {length}",
            "max": "El campo {_field_} no debe ser mayor a {length} caracteres",
            "max_value": "El campo {_field_} debe de ser {max} o menor",
            "mimes": "El campo ${field} debe ser un tipo de archivo v�lido",
            "min": "El campo {_field_} debe tener al menos {length} caracteres",
            "min_value": "El campo {_field_} debe ser {min} o superior",
            "numeric": "El campo {_field_} debe contener solo caracteres numéricos",
            "regex": "El formato del campo {_field_} no es válido",
            "required": "El campo {_field_} es obligatorio",
            "required_if": "El campo {_field_} es obligatorio",
            "size": "El campo {_field_} debe ser menor a {size}KB"
        }
    }

});

VeeValidate.localize('es');

//Error
// VeeValidate.configure({
//     classes:{
//         invalid: 'has-error'
//     }
// });

// Add a rule.
// VeeValidate.extend('date', {
//     validate(value) {
//         try {
//             let fecha = value.split("/");
//             let dateObject = new Date(fecha[2], fecha[1] - 1, fecha[0]); 
//         } catch (error) {
//             console.log("Errorsazo!!!")
//         }
//     },
//     message: 'La Fecha no es válida. Debe ser dd/mm/aaaa.'
// });

// Register the component globally.
Vue.component('validation-provider', VeeValidate.ValidationProvider);
Vue.component('validation-observer', VeeValidate.ValidationObserver);

new Vue({
    el: "#container",
    delimiters: ["[[", "]]"],
    data: {
        opcion: 1,
        checkOpciones: [],
        existeFecha: false,
        btnLoading: false,
        // Nomencladores
        provincias: {},
        municipios: {},
        grupo_edades: {},
        municipios_ubicaciones: {},
        ubicaciones: [],
        eventos: [],
        controles_foco: [],
        origenes: [],
        //Datos Parte Diario
        fecha_reporte: "",
        datos: {
            // Panel 1
            confirmados: {
                total: 0,
                sin_fid: 0,
                sintomaticos: 0,
                asintomaticos: 0,
                cubanos: 0,
                extranjeros: 0,
                masculinos: 0,
                femeninos: 0,
                contactos: 0,
                casos_aislados: 0,
                casos_comunidad: 0,
                casos_vigilancia_aps: 0,
                municipios: [],
                grupo_edades: [],
            },
            activos: {
                total: 0,
                ubicaciones: []
            },
            // Panel 2
            fallecidos: {
                covid_fallecidos: 0,
                covid_criticos: 0,
                covid_graves: 0,
                ira_graves: 0,
                ira_graves_pendiente_pcr: 0,
                altas_clinicas_covid: 0,
                altas_sospechosos: 0,
                altas_contactos: 0,
            },
            sospechosos: {
                ingresados: 0,
                comunidad: 0,
                iden_hospital: 0,
                iden_policlinico: 0,
                iden_consultorio: 0,
                iden_pesquisa: 0,
            },
            casosIRA: {
                ingresados: 0,
                comunidad: 0,
                iden_hospital: 0,
                iden_policlinico: 0,
                iden_consultorio: 0,
                iden_pesquisa: 0,
            },
            atencionIRA: {
                repor_hospital: 0,
                repor_policlinico: 0,
                repor_consultorio: 0,
            },
            // Panel 3
            pesquisa_activa: {
                porciento_pesquisada: 0,
                a_pesquisar: 0,
                presuntas_ira_identificadas: 0,
                presuntas_ira_atendidas: 0,
            },
            eventos: [],
            controles_foco: [],
            movimiento_hospitalario: {
                ingresados: 0,
                confirmados_ingresados: 0,
                sospechosos_ingresados: 0,
                contactos_ingresados: 0,
                disponibilidad_camas_ingreso: 0,
                disponibilidad_camas_graves: 0,
                disponibilidad_camas_sospechosos: 0,
                disponibilidad_camas_contactos: 0,
            },
            // Panel 4
            vigilancia: {
                muestras_tomadas: 0,
                muestras_enviadas: 0,
                muestras_eventos: 0,
                muestras_control_foco: 0,
                acumuladas_enviadas: 0,
                resultados_positivos: 0,
                resultados_confirmatorios: 0,
                resultados_negativos: 0,
                resultados_evolutivos: 0,
                resultados_inhibidos: 0,
                tiempo_promedio_salida: 0,
                tiempo_promedio_resultado: 0,
                origen: [],
            },
            muestras_pendientes: {
                con_2_dias: 0,
                con_mas_3_dias: 0,
            },
            inspeccion_sanitaria_estatal: {
                centros_visitados: 0,
                centros_inspeccionados: 0,
                inspectores_salieron: 0,
                medidas_impuestas: 0,
                municipio_no_salieron: [],
                municipio_no_medidas: [],
                municipio_no_inspectores: [],
                municipio_mayor_notificaciones: [],
            }
        },

    },
    created: function () {
        this.initCheckOptions();
        this.initProvinciasMunicipios();
        this.initGrupoEdades();
        this.initUbicaciones();
        this.initEventos();
        this.initControlesFoco();
        this.initOrigenes();


    },
    computed: {
        porcientoMenu() {
            return this.opcion * 100 / 20;
        },

    },
    // watch:{
    //     fecha_reporte: "verificarFecha"
    // },
    methods: {
        initCheckOptions() {
            for (let index = 0; index < 10; index++) {
                this.checkOpciones[index] = false;
            }
        },
        async verificarFecha() {
            await axios.post(api_url_verificar_fecha, { fecha_reporte: this.fecha_reporte })
                .then(response => {
                    if (response.data.reporte_existe) {
                        this.existeFecha = true;
                    } else {
                        this.existeFecha = false;
                    }

                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });

            return false;
        },
        async initProvinciasMunicipios() {

            await axios.get(api_url_provincia)
                .then(response => {
                    this.provincias = response.data.provincias;
                    this.municipios = response.data.municipios;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
            
        },
        async initGrupoEdades() {
            await axios.get(api_url_grupo_edades)
                .then(response => {
                    this.grupo_edades = response.data.grupo_edades;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
        },
        async initUbicaciones() {
            await axios.get(api_url_ubicacion)
                .then(response => {
                    this.municipios_ubicaciones = response.data.municipios;
                    this.ubicaciones = response.data.ubicaciones;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
        },
        async initEventos() {
            await axios.get(api_url_eventos)
                .then(response => {
                    this.eventos = response.data.eventos;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
        },
        async initControlesFoco() {
            await axios.get(api_url_controles_foco)
                .then(response => {
                    this.controles_foco = response.data.controles_foco;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
        },
        async initOrigenes() {
            await axios.get(api_url_origen)
                .then(response => {
                    this.origenes = response.data.origenes;
                })
                .catch(error => {
                    swal("Error!!", "Existen problemas cargando los datos del servidor. Vuelva a intentarlo más tarde. " + error, "error");
                });
        },
        incrementarOpcion() {
            this.opcion++;
        },
        decrementarOpcion() {
            this.opcion--;
        },
        async finalizar() {
            const self = this;
            this.fecha_reporte = document.getElementById("fecha_input").value;
            await this.verificarFecha();

            if (this.existeFecha) {
                swal({
                    title: "Advertencia!!",
                    text: "Ya existe un reporte con esa fecha. Si continúa los datos serán añadidos a los existentes. ¿Desea continuar?",
                    type: "warning",
                    showCancelButton: true,
                    // confirmButtonColor: "#DD6B55",
                    showLoaderOnConfirm: true,
                    confirmButtonText: "Continuar",
                    cancelButtonText: "Cancelar",
                    closeOnConfirm: false,
                    closeOnCancel: true,


                }, async function (isConfirm) {
                    if (isConfirm) {
                        // location.href = redirigir + "/" + res.data.factura_id;
                        // console.log("1");
                        self.guardar(true);

                    } else {
                        // event.preventDefault();
                        //swal("Cancelled !!", "Hey, your imaginary file is safe !!", "error");
                    }
                });
            } else {
                this.guardar(false);
            }
        },
        async guardar(acumular) {
            const datos_reporte = {
                fecha_reporte: this.fecha_reporte,
                datos: this.datos,
                acumular: acumular,
            };

            this.btnLoading = true;

            await axios.post(api_url_reporte, datos_reporte)
                .then(res => {
                    // console.log(res.data)

                    swal({
                        title: "Correcto!!",
                        text: "El reporte se ha creado correctamente. ¿Desea continuar?",
                        type: "success",
                        showCancelButton: true,
                        // confirmButtonColor: "#DD6B55",
                        confirmButtonText: "Continuar",
                        cancelButtonText: "Cancelar",
                        closeOnConfirm: false,
                        closeOnCancel: true
                    }, function (isConfirm) {
                        if (isConfirm) {
                            location.href = const_redirigir + "/" + res.data.idreporte;
                            // console.log("1");
                        } else {
                            // event.preventDefault();
                            //swal("Cancelled !!", "Hey, your imaginary file is safe !!", "error");
                        }
                    });
                })
                .catch(error => {
                    swal("Error!!", "Ha ocurrido un problema en el servidor. " + error, "error");
                });
            this.btnLoading = false;
        }

    },

});


