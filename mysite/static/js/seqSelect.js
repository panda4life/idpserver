$(function () {
        var $tags = $('.tags');
        var $seqInput = $('.seq');
        var $seqSelect = $('<select/>').insertBefore($seqInput).change(function() {
                $seqInput.val($seqSelect.val());
        });
        $tags.change(function() {
                $seqSelect.empty().addClass('loading');
                $.getJSON('/get-sequences.json', {'tags':$(this).val()}, function(sequences) {
                        $provSelect.removeClass('loading');
                        for(i in sequences) {
                                $seqSelect.append('<option value="'+sequences[i][0]+'">'+sequences[i][1]+'</option>');
                        }
                        $seqSelect.val($seqInput.val()).trigger('change');
                });
        }).trigger('change');
});
