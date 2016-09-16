Add the following ProxyPass to `/etc/httpd/conf.d/ssl.conf`
>`ProxyPass /bahmni/registration/magicPortLocalTrain http://10.136.23.38:8080/train`

Modify `bahmni/openmrs-module-bahmniapps/ui/app/registration/controllers/createPatientController.js` add,
> ```
>	var createPatient = function (jumpAccepted) {
>	 	return patientService.create($scope.patient, jumpAccepted).then(function (response) {
>	        var uuid = response.data.patient.uuid;
>	        console.log("patient-uuid => " + uuid);
>	        $http.get("/bahmni/registration/magicPortLocalTrain", {
>	                method: "GET",
>	                params: {"uuid":uuid},
>	                withCredentials: false
>	});