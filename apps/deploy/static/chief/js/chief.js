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

    Chief.ViewModels.LogFile = function() {
        var self = this;
        self.modal = $('#log-file-modal')
        self.modal.on('show.bs.modal', function(e) {
            self.refreshLogFile();
        });

        self.onRefreshLogFile = function(e) {
            self.refreshLogFile();
        };

        self.refreshLogFile = function() {
            $.get(Chief.config.logFileUrl).done(function(response) {
                self.modal.find('.modal-body').html(response.formatted_lines)
            });
        }
    };

})();
