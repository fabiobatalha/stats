<%block name="central_container">
      <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawVisualization);
          var options = {"pointSize": 5, "hAxis": {"title": "Months"}, "title": "fulltext and abstract accesses", "curveType": "function", "height": 500, "width": "100%", "vAxis": {"title": "Accesses"}, "legend": {"position": "rigth"}}
              function drawVisualization() {
                drawToolbar();
                query = new google.visualization.Query('/general/lines/data/?code=scl');
                query.send(queryCallback);
              }
              function queryCallback(response) {
                visualization = new google.visualization.LineChart(document.getElementById('chart'));
                visualization.draw(response.getDataTable(), options);
              }

              function drawToolbar() {
                var components = [
                    {type: 'html', datasource: '/general/lines/data/?code=scl'},
                    {type: 'csv', datasource: '/general/lines/data/?code=scl'}
                ];
                google.visualization.drawToolbar(document.getElementById('toolbar'), components);
              };

      </script>
</%block>