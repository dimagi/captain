(function() {
    "strict"

    window.Chief = {
        ViewModels: {}
    };

    Chief.ViewModels.InitiateDeploy = function() {
        var self = this;
        self.env = ko.observable(null);

        $('#deploy-modal').on('show.bs.modal', function(e) {
            var $btn = $(e.relatedTarget);
            self.env($btn.data('environment'));
        });

        self.defaultBranch = function() {
            if (self.env() === 'staging') {
                return 'autostaging';
            }
            return 'master';
        };

        self.initiateDeploy = function() {
            $('#deploy-form').submit();
        };
    };

    $('#stacktrace-modal').on('show.bs.modal', function(e) {
        var $btn = $(e.relatedTarget),
            stacktrace = $btn.data('stacktrace');

        $('#stacktrace-modal').find('.stacktrace').html(
            stacktrace.replace(/(?:\r\n|\r|\n)/g, '<br />')
        );
    });

})();
