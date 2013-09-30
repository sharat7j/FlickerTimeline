/**
 * Created with IntelliJ IDEA.
 * User: root
 * Date: 7/9/13
 * Time: 4:38 PM
 * To change this template use File | Settings | File Templates.
 */
function AttachmentCtrl($scope, $location, $timeout, Docs) {
    $(function() {
        $('#detail-form-doc').fileupload({
            dataType: 'json',
            url: '/angular-ib/app/fileupload?id=' + $location.search().id,
            add: function(e, data) {
                $scope.$apply(function(scope) {
                    // Turn the FileList object into an Array
                    for (var i = 0; i < data.files.length; i++) {
                        $scope.project.files.push(data.files[i]);
                    }
                    $scope.progressVisible = false;
                    $scope.$broadcast('fileadded',
                        { files: $scope.project.files.length });
                    $scope.toUpload = true;
                    $('button#startupload').on('startupload', function(e) {
                        data.submit();
                    });
                });
            },
            done: function(e, data) {
                //
                uploadComplete(e, data);
            },
            fail: function(e, data) {
            },
            progress: function(e, data) {
                //
            },
            progressall: function(e, data) {
                //
                uploadProgressAll(e, data);
            }
        });
    });
    $scope.$on('fileadded', function(e, parameters) {
        //
    });
    $scope.deleteCurrentAttachment = function(delid) {
        if (delid) {
            Docs.delete({ id: this.file.id });
        }
        $scope.project.files = $scope.project.files.filter(
            function(val, i, array) {
                return val !== this.file;
            },
            this);
        $scope.toUpload = $scope.project.files.some(function(val, i) {
            return !val.loaded;
        });
    };
    $scope.uploadFile = function() {
        $scope.progressVisible = true;
        $scope.percentVisible = true;
        $('button#startupload').trigger('startupload');
    };
    var waitloop, i;
    function nextwait() { // <-> hin und her
        waitloop = $timeout(function() {
            $scope.progress = i % 100 - 20;
            i += 10;
            nextwait();
        }, 500);
    }
    function uploadProgressAll(evt, data) {
        $scope.$apply(function() {
            $scope.progress = Math.round(data.loaded * 100 / data.total);
            if (data.loaded === data.total) {
                i = 0;
                $scope.percentVisible = false;
                nextwait(); // kickoff <-> hin und her
            }
        });
    }
    function uploadComplete(evt, data) {
        /* This event is raised when the server send back a response */
        $scope.$apply(function() {
            $timeout.cancel(uploadProgressAll.waitloop);
            $scope.progressVisible = false;
            $scope.toUpload = false;
            $scope.project.files =
                $scope.project.files.map(function(file, index, array) {
                    var x = data.result.filter(function(f, i) {
                        return f.name == file.name;
                    });
                    if (x.length > 0) {
                        file.url = x[0].url;
                    }
                    if (!file.loaded) {
                        file.loaded = true;
                    }
                    return file;
                });
            //alert(evt.target.responseText);
        });
    }
    function uploadFailed(evt) {
        alert('There was an error attempting to upload the file.');
    }
    function uploadCanceled(evt) {
        $scope.$apply(function() {
            $scope.progressVisible = false;
        });
        alert('The upload has been canceled by the user or the browser ' +
            'dropped the connection.');
    }
}
AttachmentCtrl.$inject = ['$scope', '$location', '$timeout', 'Docs'];