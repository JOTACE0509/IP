### Consulta 1 ###

// Subconjunto 1: Obras que possuem "FTIR"
const subset1 = db.articles_data.find({
  $or: [
    { abstract: { $regex: "\\bFTIR\\b", $options: "i" } },
    { title: { $regex: "\\bFTIR\\b", $options: "i" } },
    { "keywords.authorKeywords": { $regex: "\\bFTIR\\b", $options: "i" } }
  ]
}).toArray();

// Subconjunto 2: Obras que possuem "microFTIR", "micro-FTIR", "u-FTIR", "uFTIR", "µ-FTIR", "µFTIR"
const subset2 = db.articles_data.find({
  $or: [
    { abstract: { $regex: "\\bmicro[-]?FTIR\\b", $options: "i" } },
    { abstract: { $regex: "\\bu[-]?FTIR\\b", $options: "i" } },
    { abstract: { $regex: "\\bµ[-]?FTIR\\b", $options: "i" } },
    { title: { $regex: "\\bmicro[-]?FTIR\\b", $options: "i" } },
    { title: { $regex: "\\bu[-]?FTIR\\b", $options: "i" } },
    { title: { $regex: "\\bµ[-]?FTIR\\b", $options: "i" } },
    { "keywords.authorKeywords": { $regex: "\\bmicro[-]?FTIR\\b", $options: "i" } },
    { "keywords.authorKeywords": { $regex: "\\bu[-]?FTIR\\b", $options: "i" } },
    { "keywords.authorKeywords": { $regex: "\\bµ[-]?FTIR\\b", $options: "i" } }
  ]
}).toArray();

// Subconjunto 3: Obras que possuem "%FTIR%" (qualquer coisa antes ou depois de "FTIR")
const subset3 = db.articles_data.find({
  $and: [
    {
      $or: [
        { abstract: { $regex: "FTIR", $options: "i" } },
        { title: { $regex: "FTIR", $options: "i" } },
        { "keywords.authorKeywords": { $regex: "FTIR", $options: "i" } }
      ]
    },
    {
      $nor: [
        { abstract: { $regex: "\\bFTIR\\b", $options: "i" } },
        { title: { $regex: "\\bFTIR\\b", $options: "i" } },
        { "keywords.authorKeywords": { $regex: "\\bFTIR\\b", $options: "i" } }
      ]
    }
  ]
}).toArray();

// Subconjunto 4: Obras que possuem "microinfrared" ou "micro-infrared"
const subset4 = db.articles_data.find({
  $or: [
    { abstract: { $regex: "\\bmicro[-]?infrared\\b", $options: "i" } },
    { title: { $regex: "\\bmicro[-]?infrared\\b", $options: "i" } },
    { "keywords.authorKeywords": { $regex: "\\bmicro[-]?infrared\\b", $options: "i" } }
  ]
}).toArray();

// Exibindo os subconjuntos
print("Subconjunto 1 - FTIR:", JSON.stringify(subset1, null, 2));
print("Subconjunto 2 - microFTIR variations:", JSON.stringify(subset2, null, 2));
print("Subconjunto 3 - %FTIR%:", JSON.stringify(subset3, null, 2));
print("Subconjunto 4 - microinfrared variations:", JSON.stringify(subset4, null, 2));


### consulta 2 ###

db.articles_data.aggregate([
  {
    $facet: {
      "Subconjunto_1_Somente_FTIR": [
        {
          $match: {
            $or: [
              { abstract: { $regex: "\\bFTIR\\b", $options: "i" } },
              { title: { $regex: "\\bFTIR\\b", $options: "i" } },
              { "keywords.authorKeywords": { $regex: "\\bFTIR\\b", $options: "i" } }
            ]
          }
        },
        {
          $unwind: "$corresponding_addresses"
        },
        {
          $project: {
            _id: 0,
            country: "$corresponding_addresses.country",
            region: "$corresponding_addresses.region",
            sub_region: "$corresponding_addresses.sub_region",
            intermediate_region: "$corresponding_addresses.intermediate_region",
          }
        }
      ],
      "Subconjunto_2_FTIR_Like_And_Microinfrared": [
        {
          $match: {
            $and: [
              {
                $or: [
                  { abstract: { $regex: "FTIR", $options: "i" } },
                  { title: { $regex: "FTIR", $options: "i" } },
                  { "keywords.authorKeywords": { $regex: "FTIR", $options: "i" } },
                  { abstract: { $regex: "microinfrared", $options: "i" } },
                  { title: { $regex: "microinfrared", $options: "i" } },
                  { "keywords.authorKeywords": { $regex: "microinfrared", $options: "i" } },
                  { abstract: { $regex: "micro-infrared", $options: "i" } },
                  { title: { $regex: "micro-infrared", $options: "i" } },
                  { "keywords.authorKeywords": { $regex: "micro-infrared", $options: "i" } }
                ]
              },
              {
                $nor: [
                  { abstract: { $regex: "\\bFTIR\\b", $options: "i" } },
                  { title: { $regex: "\\bFTIR\\b", $options: "i" } },
                  { "keywords.authorKeywords": { $regex: "\\bFTIR\\b", $options: "i" } }
                ]
              }
            ]
          }
        },
        {
          $unwind: "$corresponding_addresses"
        },
        {
          $project: {
            _id: 0,
            country: "$corresponding_addresses.country",
            region: "$corresponding_addresses.region",
            sub_region: "$corresponding_addresses.sub_region",
            intermediate_region: "$corresponding_addresses.intermediate_region",
          }
        }
      ]
    }
  }
]);



### consulta 4 ###

db.articles_data.aggregate([
    {
      // Filtra apenas os documentos publicados entre 2014 e 2023
      $match: {
        "source.publishYear": { $gte: 2014, $lte: 2023 }
      }
    },
    {
      // Agrupa por ano de publicação e nome do jornal, contando o número de publicações
      $group: {
        _id: { year: "$source.publishYear", journal: "$Journal Information.Journal Name" },
        publicationCount: { $sum: 1 }
      }
    },
    {
      // Reorganiza o formato do documento para facilitar a visualização
      $project: {
        _id: 0,
        year: "$_id.year",
        journal: "$_id.journal",
        publicationCount: 1
      }
    },
    {
      // Ordena por ano e, dentro de cada ano, pelo número de publicações (descendente)
      $sort: { year: 1, publicationCount: -1 }
    },
    {
      // Agrupa por ano e mantém apenas os Top 10 jornais com mais publicações em cada ano
      $group: {
        _id: "$year",
        topJournals: {
          $push: {
            journal: "$journal",
            publicationCount: "$publicationCount"
          }
        }
      }
    },
    {
      // Reduz a lista para apenas os 10 primeiros jornais por ano
      $project: {
        year: "$_id",
        topJournals: { $slice: ["$topJournals", 10] }
      }
    },
    {
      // Ordena os resultados por ano
      $sort: { year: 1 }
    }
  ]).forEach(doc => {
    print(`Ano: ${doc.year}`);
    doc.topJournals.forEach((journal, index) => {
      print(`${index + 1}. ${journal.journal} - ${journal.publicationCount} publicações`);
    });
    print("------------------------------------------------------");
  });
  


### consulta 5 ###

db.articles_data.aggregate([
    {
      // Filtra os artigos publicados entre 2014 e 2023
      $match: {
        "source.publishYear": { $gte: 2014, $lte: 2023 }
      }
    },
    {
      // Agrupa por ano e por artigo, somando as citações e coletando as informações necessárias
      $project: {
        _id: 0,
        year: "$source.publishYear",
        title: "$title",
        citations: "$citations.count",
        corresponding_address: {
          country: "$corresponding_addresses.country",
          region: "$corresponding_addresses.region",
          intermediate_region: "$corresponding_addresses.intermediate_region",
          sub_region: "$corresponding_addresses.sub_region"
        }
      }
    },
    {
      // Ordena os artigos dentro de cada ano pelo número de citações, de forma decrescente
      $sort: { year: 1, citations: -1 }
    },
    {
      // Agrupa por ano e mantém apenas os 10 artigos mais citados
      $group: {
        _id: "$year",
        topArticles: {
          $push: {
            title: "$title",
            citations: "$citations",
            corresponding_address: "$corresponding_address"
          }
        }
      }
    },
    {
      // Reduz a lista para os Top 10 artigos mais citados por ano
      $project: {
        year: "$_id",
        topArticles: { $slice: ["$topArticles", 10] }
      }
    },
    {
      // Ordena por ano para a exibição final
      $sort: { year: 1 }
    }
  ]).forEach(doc => {
    print(`Ano: ${doc.year}`);
    doc.topArticles.forEach((article, index) => {
      print(`${index + 1}. Artigo: ${article.title}`);
      print(`   Citações: ${article.citations}`);
      print(`   País: ${article.corresponding_address.country}`);
      print(`   Região: ${article.corresponding_address.region}`);
      print(`   Região Intermediária: ${article.corresponding_address.intermediate_region}`);
      print(`   Sub-Região: ${article.corresponding_address.sub_region}`);
    });
    print("------------------------------------------------------");
  });
  

