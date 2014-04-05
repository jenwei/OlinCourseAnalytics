//mongoose setup
var mongoose = require('mongoose');

//patient schema
var patientSchema = mongoose.Schema({
    patientName: String,
});

//order schema
var mediatorSchema = mongoose.Schema({
    mediatorName: String,
});


//make the schemas into models
var Patient = mongoose.model('Patient', ingredientSchema);
var Mediator = mongoose.model('Mediator', orderSchema);

//so we can use it in routes , etc
exports.Patient = Patient;
exports.Mediator = Mediator;