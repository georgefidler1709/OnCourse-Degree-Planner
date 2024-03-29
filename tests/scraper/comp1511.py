text = '''
<!DOCTYPE html>
<html lang="en">

<head>
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
	  				<meta charset="utf-8">
<title>Handbook - Course - Programming Fundamentals - COMP1511</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	  <meta name="description" content="Programming Fundamentals">

      <meta name="keywords" content="computer science, computing, debugging, linux, programming, software, testing">
  
  <meta name="author" content="School of Computer Science and Engineering">

<link href="https://fonts.googleapis.com/css?family=Roboto:300,400,400i,500,500i,700,700i" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- TODO this should be in the main package -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/16.7.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/16.7.0/umd/react-dom.production.min.js"></script>

<!-- Courseloop-ui / handbook includes -->




	<!-- Live -->
	<link href="https://courseloop-ui.s3.amazonaws.com/handbook/unsw/unswPRODUCTION/assets/all.css?v=2019-11-11-22-9" rel="stylesheet">
	<script src="https://courseloop-ui.s3.amazonaws.com/handbook/unsw/unswPRODUCTION/assets/all.js?v=2019-11-11-22-9"></script>

<!-- Remove when we no longer have skeleton elements -->
<link rel="stylesheet" href="/application/themes/page-details/css/skeleton.css">

<!-- Temp theme for murdoch stuff -->

<!-- Styles for printing page -->
<link rel="stylesheet" href="/application/theme_files/css/print.css">

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GTM-5JB423"></script>

<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

// gtag('config', '${host.googleAnalytics}');
gtag('config', 'GTM-5JB423');
</script>
	
    
					
								
	<script>
		(function(){
						const orgUnits = {};
			const locations = {"196234bfdb0f8b005012ff0dbf961912":"Sydney","007d533c4f441b009e2bfd501310c712":"Paddington","6ecfe5f4db4a5b0014c5f4e9bf961926":"Paddington","d7470b6c4f115b404aa6eb4f0310c79b":"Canberra","6a49b4034f4d97404aa6eb4f0310c79b":"Kensington","62b1be25dbc4d70014c5f4e9bf9619ef":"Randwick"};
			const helptext = [{"description":"A component of an academic program, normally of one term/semester in duration, with a specific credit value.","term":"Course","type":"helptext"},{"description":"An award where two or more programs are studied at the same time, resulting in two separate qualifications.","term":"Dual Award Program","type":"helptext"},{"description":"A level of study that leads to the award of a Graduate Certificate, Graduate Diploma, Masters Degree or Doctorate.","term":"Postgraduate","type":"helptext"},{"description":"A specified sequence of study in a discipline or sub discipline area within a program.  More than one major may be completed within a program.","term":"Major","type":"helptext"},{"description":"A course students are prevented from taking, because they have academic content in common with courses for which the student has previously been granted credit.","term":"Exclusion Courses","type":"helptext"},{"description":"The umbrella term for a defined area of disciplinary study. In undergraduate programs, they are majors and minors. In postgraduate coursework programs they are referred to as specialisations. \r\n\r\n","term":"Specialisation","type":"helptext"},{"description":"Typically refers to face to face on-campus contact hours per week.","term":"Indicative contact hours","type":"tooltip"},{"description":"An approved set of requirements, courses and/or supervised research into which a student is admitted. In some cases, this will lead to an award of UNSW.","term":"Program","type":"helptext"},{"description":"A level of study which involves a student independently researching a specific topic under the guidance of a supervisor and producing a thesis or report. Some research programs involve a coursework component.","term":"Research","type":"helptext"},{"description":"A level of study that leads to the award of a Diploma, Advanced Diploma, Associate Degree or a Bachelor Degree (pass or honours).","term":"Undergraduate","type":"helptext"},{"description":"Courses taken outside of the home faculty to complement more specialised learning. Students are still subject to Faculty and program specific conditions/requirements on General Education selection.","term":"General Education","type":"helptext"},{"description":"A specified field of study within a discipline or sub-discipline, smaller in size and scope than a major. ","term":"Minor","type":"helptext"},{"description":"An academic teaching period of between 10-13 weeks in duration.","term":"Semester/Term","type":"helptext"},{"description":"The highest level of learning in an undergraduate program. It typically includes a research component. Honours is available in two modes: separate year honours and embedded honours.","term":"Honours","type":"helptext"},{"description":"Qualification upon completion (all awards offered by UNSW are accredited by UNSW and align with the Australian Qualifications Framework).","term":"Award(s)","type":"helptext"},{"description":"(UOC) A value assigned to programs and courses indicating duration and workload, e.g. class contact hours, other learning activities, preparation and time spent on all assessable works. ","term":"Units of Credit","type":"helptext"},{"description":"An approved agreement which enables students to progress in a defined pathway from one qualification to another with credit.","term":"Articulation Arrangements","type":"helptext"},{"description":"The primary academic unit in which related disciplines of teaching and research are conducted.","term":"Faculty","type":"helptext"},{"description":"An academic teaching period of between 10-13 weeks in duration.","term":"Offering Periods","type":"helptext"},{"description":"A course deemed to be equal in academic content to another course. You will need to choose a different course if you have successfully completed the equivalent course.","term":"Equivalent Courses","type":"helptext"},{"description":"The academic unit responsible for teaching in disciplines or subject areas (school is part of a Faculty)","term":"School","type":"helptext"},{"description":"The delivery option(s) by which a course or program is offered.","term":"Delivery Mode","type":"helptext"},{"description":"An award where two or more programs are studied at the same time, resulting in two separate qualifications.","term":"Double Degree","type":"helptext"},{"description":"An academic teaching period of between 10-13 weeks in duration.","term":"Offering Terms","type":"helptext"},{"description":"Knowledge, skills and their applications, behaviours and practices that students develop during their time at UNSW.","term":"Graduate Capabilities","type":"helptext"},{"description":"Units of Credit","term":"UOC","type":"helptext"}];
			const messages = {
			  enrolment_message: 'Not admitting new students'
			}
			window.config.setInstance({org: "CL", orgs: orgUnits, locations: locations, messages: messages, helptext: helptext});
		})()	

    if (window.globalFeatures.override) {
      const CLFeatureFlags = {"CL.year_value":"2020","CL.year_switcher_toggle":"true","CL.ga_id":"GTM-5JB423"};
      let formattedFlagsObject = {}
      Object.keys(CLFeatureFlags).forEach(function(key) {
        if(CLFeatureFlags[key] === "true" || CLFeatureFlags[key] == "false") {
          const _key = key.split('.')[1];
          formattedFlagsObject = {
            ...formattedFlagsObject,
            [_key]: {
              on: CLFeatureFlags[key] === "true" ? true : false
            }
          };
        }
      });
      window.globalFeatures.override(formattedFlagsObject);
    }
	</script>
</head>
  <body class="default-page-details-template" style="overflow-x:hidden" id="default-page-details-template">
<span class="sr-only" id="tooltipMessenger" aria-live="assertive"></span>
			



<header class="t-header" role="banner" aria-label="Handbook Logo, Search, main navigation and secondary navigation">
  
<div class="a-secondary-nav p-bottom-0 hide-sm hide-xs" role="navigation" aria-label="Secondary Navigation Links">
  <div class="a-wrapper" data-hbui="a-nav-container" style="display:inherit; padding-bottom: 0.2rem">
    <div class="a-nav-links">
                  
      <a href="http://www.handbook.unsw.edu.au/general/2018/SSAPO/previousEditions.html" target="_blank">Pre-2019 Handbook</a>
                  
      <a href="https://my.unsw.edu.au/" target="_blank">My UNSW</a>
                  
      <a href="https://student.unsw.edu.au/" target="_blank">Current Student</a>
                  
      <a href="https://www.futurestudents.unsw.edu.au/" target="_blank">Future Student</a>
                  
      <a href="https://research.unsw.edu.au/" target="_blank">Research</a>
                  
      <a href="https://student.unsw.edu.au/new-calendar" target="_blank">UNSW 3+</a>
                  
      <a href="http://timetable.unsw.edu.au" target="_blank">Class Timetable</a>
          </div>
    <button tabindex="0" data-hbui="a-nav-bookmark" class="a-nav-bookmark" id="a-nav-bookmark-link" aria-label="Click to toggle My Lists" aria-haspopup="true">
      <i class="a-icon gets-notified" id="a-nav-bookmark-icon" aria-hidden="true">bookmark</i>
    </button>
    <div tabindex="-1" data-hbui="a-nav-sub-links-container" class="a-nav-sub-links with-arrow hidden" aria-hidden="true">
      <h2 tabindex="0" class="m-top-1 m-left-1 m-right-1 heading h3" aria-label="My Lists: a list of of your saved academic items.">My Lists</h2>
      <div data-hbui="a-nav-sub-links-list" tabindex="-1" class="a-nav-sub-links-list " aria-controlledby="a-nav-bookmark-link">
      </div>
    </div>
          </div>
</div>
  <div class="a-wrapper t-header__wrapper">
    <div class="t-logo-container">
      <a href="https://www.unsw.edu.au/" target="_blank" title="Click here to go to UNSW website">
        <img class="a-logo" src="/application/theme_files/assets/unsw-logo.svg" alt="UNSW Logo" />
      </a>
    </div>
        <!-- Place additional header html here -->

<div class="t-mini-search-header-container">
  <h1 tabindex="0" class="t-header__heading h3">Handbook</h1>
  <div class="m-mini-search-container" id="mini-search"></div>
</div>

<script>
  var initialState = {
    ADDITIONAL_SEARCH_PHRASE: '', // include a certain phrase to join with whatever the user searches for. Seperate values with spaces e.g. '2018 Courses'
    SEE_ALL_RESULTS_LABEL: 'See all results',
    SEE_ALL_RESULTS_URL: '/search',
    ADVANCED_SEARCH_LABEL: 'Advanced search',
    ADVANCED_SEARCH_URL: '/search',
    NO_RESULTS_LABEL: 'No results',
    PLACEHOLDER_TEXT: 'Search here or hit Enter for advanced search',
    CON_HOST: 'ce0bf305-2092-4d52-bd3b-b63d8e576981',
    SEARCH_FILTERS_URL:'/api/content/render/false/type/json/query/+contentType:static_content%20 +static_content.key:*search_filter*%20+static_content.addToSecondarySearch:1%20+(conhost:[[__CON_HOST__]]%20conhost:SYSTEM_HOST)%20+languageId:1%20+deleted:false%20+working:true/orderby/static_content.order%20asc',
    CHOICE_SET_URL: '/api/content/render/false/type/json/query/+contentType:choice_set%20+(conhost:[[__CON_HOST__]]%20conhost:SYSTEM_HOST)%20+languageId:1%20+deleted:false%20+working:true/orderby/modDate%20desc',
    ACADEMIC_ITEMS: [{
      value: 'course',
      label: 'Program',
      contentType: 'CL.course_search_filter',
    }, {
      value: 'aos',
      label: 'Specialisation',
      contentType: 'CL.aos_search_filter',
    }, {
      value: 'subject',
      label: 'Course',
      contentType: 'CL.subject_search_filter',
    }],
    DISPLAY_ADVANCED_FILTERS: false,
    validYears: [{"label":"2019","value":"2019"},{"label":"2020","value":"2020"}],
    CURRENT_YEAR: "2020",
  };
  ReactDOM.render(
    React.createElement(handbook.MiniSearch, initialState),
    document.querySelector('#mini-search')
  );
</script>

    
    <button class="a-toothpick gets-notified" data-hbui="hamburger-toggle" tabindex="0" aria-label="Open Main Navigation Menu" role="navigation">
      <span class="a-toothpick__label hide-sm hide-xs">Browse</span>
      <i class="a-icon" aria-hidden="true">menu</i>
    </button>
  </div>
</header>
	
	


  <div>

    







<div data-hbui="hamburger-menu" class="a-sticky a-hamburger no-print" role="navigation" tabindex="-1" aria-hidden="true" aria-label="Main Site Navigation">
  <div data-hbui="hamburger-menu-main" class="a-bun">
    <div class="a-tomato">
      <button class="a-icon" data-hbui="hamburger-close" tabindex="-1" aria-label="Close Main Navigation Menu"><span aria-hidden="true">close</span></button>
    </div>
    <div class="a-cheese" data-hbui="scrollable" tabindex="-1">
      <div data-hbui="hamburger-menu-item" class="a-sauce bookmark" >
        <button class="a-lettuce level-one" data-hbui="hamburger-next" tabindex="-1" aria-label="Open Sub Menu for My Lists">
          <span class="a-icon a-pickle level-two" aria-hidden="true">bookmark</span>
          <h2 class="h4" aria-hidden="true">My Lists <span data-hbui="bookmark-list-count"></span></h2>
          <i class="a-icon a-pickle" aria-hidden="true">navigate_next</i>
        </button>
        <div data-hbui="hamburger-menu-sub" class="a-patty" tabindex="-1" aria-hidden="true">
          <div class="a-tomato">
            <button class="a-icon a-pickle level-two" data-hbui="hamburger-back" tabindex="-1" aria-label="Back to Main Menu"><span aria-hidden="true">arrow_back</span></button>
            <h3 class="h4">My Lists</h3>
          </div>
          <div data-hbui="hamburger-menu-bookmarks-container" tabindex="-1" aria-hidden="true">
          </div>
        </div>
      </div>

      <hr class="a-onion" tabindex="-1">
      <span class="p-top-1 p-left-1 p-bottom-1 font-weight-heavy" style="display:block;">Browse Handbook</span>
              
         
        <div data-hbui="hamburger-menu-item" class="a-sauce">
          <button class="a-lettuce level-one" data-hbui="hamburger-next" tabindex="-1" aria-label="Open Sub Menu for Area of Interest" aria-haspopup="true">
            <h4   aria-hidden="true">Area of Interest</h4>
            <i class="a-icon a-pickle" aria-hidden="true">navigate_next</i>
          </button>
          <div data-hbui="hamburger-menu-sub" class="a-patty" tabindex="-1" aria-hidden="true">
            <div class="a-tomato">
              <button class="a-icon a-pickle level-two" data-hbui="hamburger-back" tabindex="-1" aria-label="Back to Main Menu"><span aria-hidden="true">arrow_back</span></button>
              <h4>Area of Interest <span class="sr-only">Sub Menu</span></h4>
            </div>

            <div data-hbui="scrollable" tabindex="-1">
                                          
  
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/ArchitectureAndBuilding/browse?interest_value=68b44253db96df002e4c126b3a961980
" target="_self" tabindex="-1">
          <h4>Architecture and Building</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/BusinessAndManagement/browse?interest_value=dd350293db96df002e4c126b3a961909
" target="_self" tabindex="-1">
          <h4>Business and Management</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/CreativeArts/browse?interest_value=c175c653db96df002e4c126b3a9619f3
" target="_self" tabindex="-1">
          <h4>Creative Arts</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/Education/browse?interest_value=f9158253db96df002e4c126b3a961953
" target="_self" tabindex="-1">
          <h4>Education</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/EngineeringAndRelatedTechnologies/browse?interest_value=8a948253db96df002e4c126b3a961950
" target="_self" tabindex="-1">
          <h4>Engineering and Related Technologies</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/EnvironmentalAndRelatedStudies/browse?interest_value=4ee48253db96df002e4c126b3a961926
" target="_self" tabindex="-1">
          <h4>Environmental and Related Studies</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/Health/browse?interest_value=34054293db96df002e4c126b3a9619ee
" target="_self" tabindex="-1">
          <h4>Health</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/HumanitiesAndLaw/browse?interest_value=0c554e13db96df002e4c126b3a9619f5
" target="_self" tabindex="-1">
          <h4>Humanities and Law</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/InformationTechnology/browse?interest_value=cd74ce13db96df002e4c126b3a96194f
" target="_self" tabindex="-1">
          <h4>Information Technology</h4>
        </a>
      </div>
      
          <div class="a-sauce">
        <a class="a-lettuce level-two" href="/NaturalAndPhysicalSciences/browse?interest_value=b7b2ce13db96df002e4c126b3a96194c
" target="_self" tabindex="-1">
          <h4>Natural and Physical Sciences</h4>
        </a>
      </div>
                                            </div>
          </div>
        </div>

                      
         
        <div data-hbui="hamburger-menu-item" class="a-sauce">
          <button class="a-lettuce level-one" data-hbui="hamburger-next" tabindex="-1" aria-label="Open Sub Menu for Faculty" aria-haspopup="true">
            <h4   aria-hidden="true">Faculty</h4>
            <i class="a-icon a-pickle" aria-hidden="true">navigate_next</i>
          </button>
          <div data-hbui="hamburger-menu-sub" class="a-patty" tabindex="-1" aria-hidden="true">
            <div class="a-tomato">
              <button class="a-icon a-pickle level-two" data-hbui="hamburger-back" tabindex="-1" aria-label="Back to Main Menu"><span aria-hidden="true">arrow_back</span></button>
              <h4>Faculty <span class="sr-only">Sub Menu</span></h4>
            </div>

            <div data-hbui="scrollable" tabindex="-1">
                                                                                               
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/DvcacademicBoardOfStudies/browse?id=5fa56ceb4f0093004aa6eb4f0310c7b3" target="_self" tabindex="-1">
            <h4>DVC (Academic) Board of Studies</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfArtDesign/browse?id=57a56ceb4f0093004aa6eb4f0310c7af" target="_self" tabindex="-1">
            <h4>Faculty of Art & Design</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfArtsAndSocialSciences/browse?id=d7a56ceb4f0093004aa6eb4f0310c7ac" target="_self" tabindex="-1">
            <h4>Faculty of Arts and Social Sciences</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfBuiltEnvironment/browse?id=5fa56ceb4f0093004aa6eb4f0310c7ae" target="_self" tabindex="-1">
            <h4>Faculty of Built Environment</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfEngineering/browse?id=5fa56ceb4f0093004aa6eb4f0310c7af" target="_self" tabindex="-1">
            <h4>Faculty of Engineering</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfLaw/browse?id=57a56ceb4f0093004aa6eb4f0310c7b0" target="_self" tabindex="-1">
            <h4>Faculty of Law</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfMedicine/browse?id=5fa56ceb4f0093004aa6eb4f0310c7b0" target="_self" tabindex="-1">
            <h4>Faculty of Medicine</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/FacultyOfScience/browse?id=57a56ceb4f0093004aa6eb4f0310c7ae" target="_self" tabindex="-1">
            <h4>Faculty of Science</h4>
          </a>
        </div>
                                                                                                                                                                                                                                                                                              
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/UnswBusinessSchool/browse?id=5a3a1d4f4f4d97404aa6eb4f0310c77a" target="_self" tabindex="-1">
            <h4>UNSW Business School</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/UnswCanberraAtAdfa/browse?id=5fa56ceb4f0093004aa6eb4f0310c7ad" target="_self" tabindex="-1">
            <h4>UNSW Canberra at ADFA</h4>
          </a>
        </div>
                
                    <div class="a-sauce">
          <a class="a-lettuce level-two" href="/UnswGlobal/browse?id=a9321f614ffd57009106fd501310c7eb" target="_self" tabindex="-1">
            <h4>UNSW Global</h4>
          </a>
        </div>
                                                          </div>
          </div>
        </div>

                      
         
        <div data-hbui="hamburger-menu-item" class="a-sauce">
          <button class="a-lettuce level-one" data-hbui="hamburger-next" tabindex="-1" aria-label="Open Sub Menu for Subject Area" aria-haspopup="true">
            <h4   aria-hidden="true">Subject Area</h4>
            <i class="a-icon a-pickle" aria-hidden="true">navigate_next</i>
          </button>
          <div data-hbui="hamburger-menu-sub" class="a-patty" tabindex="-1" aria-hidden="true">
            <div class="a-tomato">
              <button class="a-icon a-pickle level-two" data-hbui="hamburger-back" tabindex="-1" aria-label="Back to Main Menu"><span aria-hidden="true">arrow_back</span></button>
              <h4>Subject Area <span class="sr-only">Sub Menu</span></h4>
            </div>

            <div data-hbui="scrollable" tabindex="-1">
                                                <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Accounting/browse?sa=b4cecfec4fcb5b00eeb3eb4f0310c7eb" target="_self" tabindex="-1">
        <h4>ACCT: Accounting</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ActuarialStudies/browse?sa=7cce03204f0f5b00eeb3eb4f0310c709" target="_self" tabindex="-1">
        <h4>ACTL: Actuarial Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ArtAndDesign/browse?sa=b8ce03204f0f5b00eeb3eb4f0310c70e" target="_self" tabindex="-1">
        <h4>ADAD: Art and Design</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/AerospaceEngineering/browse?sa=c5ce03204f0f5b00eeb3eb4f0310c713" target="_self" tabindex="-1">
        <h4>AERO: Aerospace Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Anatomy/browse?sa=05ce03204f0f5b00eeb3eb4f0310c718" target="_self" tabindex="-1">
        <h4>ANAT: Anatomy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Architecture/browse?sa=41ce03204f0f5b00eeb3eb4f0310c71d" target="_self" tabindex="-1">
        <h4>ARCH: Architecture</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/DisciplinaryAndInterdisciplinaryHumanities/browse?sa=8dce03204f0f5b00eeb3eb4f0310c721" target="_self" tabindex="-1">
        <h4>ARTS: Disciplinary and Interdisciplinary Humanities</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/NuraGiliindigenousPrograms/browse?sa=c9ce03204f0f5b00eeb3eb4f0310c726" target="_self" tabindex="-1">
        <h4>ATSI: Nura Gili (Indigenous Programs)</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Aviation/browse?sa=09ce03204f0f5b00eeb3eb4f0310c72b" target="_self" tabindex="-1">
        <h4>AVEN: Aviation</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Aviation/browse?sa=45ce03204f0f5b00eeb3eb4f0310c730" target="_self" tabindex="-1">
        <h4>AVIA: Aviation</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Aviation/browse?sa=735f5e79dbf393000595c4048a961909" target="_self" tabindex="-1">
        <h4>AVIF: Aviation</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Aviation/browse?sa=bb5f5e79dbf393000595c4048a96190e" target="_self" tabindex="-1">
        <h4>AVIG: Aviation</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BiotechnologyBiomolecularSciences/browse?sa=81ce03204f0f5b00eeb3eb4f0310c735" target="_self" tabindex="-1">
        <h4>BABS: Biotechnology & Biomolecular Sciences</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BiologicalEarthEnvironmentalScience/browse?sa=cdce03204f0f5b00eeb3eb4f0310c739" target="_self" tabindex="-1">
        <h4>BEES: Biological, Earth & Environmental Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BeInterdisciplinaryLearning/browse?sa=0dce03204f0f5b00eeb3eb4f0310c73e" target="_self" tabindex="-1">
        <h4>BEIL: BE Interdisciplinary Learning</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BuiltEnvironment/browse?sa=49ce03204f0f5b00eeb3eb4f0310c743" target="_self" tabindex="-1">
        <h4>BENV: Built Environment</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Bioinformatics/browse?sa=95ce03204f0f5b00eeb3eb4f0310c748" target="_self" tabindex="-1">
        <h4>BINF: Bioinformatics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Biochemistry/browse?sa=d1ce03204f0f5b00eeb3eb4f0310c74d" target="_self" tabindex="-1">
        <h4>BIOC: Biochemistry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BiomedicalEngineering/browse?sa=11ce03204f0f5b00eeb3eb4f0310c752" target="_self" tabindex="-1">
        <h4>BIOM: Biomedical Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BiologicalScience/browse?sa=5dce03204f0f5b00eeb3eb4f0310c756" target="_self" tabindex="-1">
        <h4>BIOS: Biological Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Biotechnology/browse?sa=99ce03204f0f5b00eeb3eb4f0310c75b" target="_self" tabindex="-1">
        <h4>BIOT: Biotechnology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Building/browse?sa=d5ce03204f0f5b00eeb3eb4f0310c760" target="_self" tabindex="-1">
        <h4>BLDG: Building</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/CareerDevelopment/browse?sa=4c95ede9db1b7f00038cc4048a96195e" target="_self" tabindex="-1">
        <h4>CDEV: Career Development</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ChemicalEngineeringAndIndustrialChemistry/browse?sa=15ce03204f0f5b00eeb3eb4f0310c765" target="_self" tabindex="-1">
        <h4>CEIC: Chemical Engineering and Industrial Chemistry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Chemistry/browse?sa=51ce03204f0f5b00eeb3eb4f0310c76a" target="_self" tabindex="-1">
        <h4>CHEM: Chemistry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ChemicalEngineering/browse?sa=9dce03204f0f5b00eeb3eb4f0310c76e" target="_self" tabindex="-1">
        <h4>CHEN: Chemical Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ClimateScience/browse?sa=d9ce03204f0f5b00eeb3eb4f0310c773" target="_self" tabindex="-1">
        <h4>CLIM: Climate Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ComputationalDesign/browse?sa=19ce03204f0f5b00eeb3eb4f0310c778" target="_self" tabindex="-1">
        <h4>CODE: Computational Design</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/DevelopmentStudies/browse?sa=f75f5e79dbf393000595c4048a961913" target="_self" tabindex="-1">
        <h4>COMD: Development Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Commerce/browse?sa=55ce03204f0f5b00eeb3eb4f0310c77d" target="_self" tabindex="-1">
        <h4>COMM: Commerce</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ComputerScience/browse?sa=91ce03204f0f5b00eeb3eb4f0310c782" target="_self" tabindex="-1">
        <h4>COMP: Computer Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ConstructionManagement/browse?sa=fb5f5e79dbf393000595c4048a961924" target="_self" tabindex="-1">
        <h4>CONS: Construction Management</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Criminology/browse?sa=ddce03204f0f5b00eeb3eb4f0310c786" target="_self" tabindex="-1">
        <h4>CRIM: Criminology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/CreativePractice/browse?sa=dbf77de7dbbce7040595c4048a961934" target="_self" tabindex="-1">
        <h4>CRTV: Creative practice</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/CivilAndEnvironmentalEngineering/browse?sa=1dce03204f0f5b00eeb3eb4f0310c78b" target="_self" tabindex="-1">
        <h4>CVEN: Civil and Environmental Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/DataScience/browse?sa=69ce03204f0f5b00eeb3eb4f0310c790" target="_self" tabindex="-1">
        <h4>DATA: Data Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/DesignNext/browse?sa=ed7b2e13dba840507cdee3334a961902" target="_self" tabindex="-1">
        <h4>DESN: Design Next</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GlobalDiplomaBusiness/browse?sa=f1db6e13dba840507cdee3334a961975" target="_self" tabindex="-1">
        <h4>DPBS: Global Diploma - Business</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GlobalDiplomaGeneralEducation/browse?sa=fd0f7626db6c63003167e7148a961953" target="_self" tabindex="-1">
        <h4>DPGE: Global Diploma - General Education</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GlobalDiplomaStem/browse?sa=048ebaa2db6c63003167e7148a961964" target="_self" tabindex="-1">
        <h4>DPST: Global Diploma - STEM</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Economics/browse?sa=e1ce03204f0f5b00eeb3eb4f0310c79a" target="_self" tabindex="-1">
        <h4>ECON: Economics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/EducationStudies/browse?sa=21ce03204f0f5b00eeb3eb4f0310c79f" target="_self" tabindex="-1">
        <h4>EDST: Education Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ElectricalEngineering/browse?sa=6dce03204f0f5b00eeb3eb4f0310c7a3" target="_self" tabindex="-1">
        <h4>ELEC: Electrical Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/EngineeringInterdisciplinary/browse?sa=a9ce03204f0f5b00eeb3eb4f0310c7a8" target="_self" tabindex="-1">
        <h4>ENGG: Engineering interdisciplinary</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/EnvironmentalStudies/browse?sa=e5ce03204f0f5b00eeb3eb4f0310c7ad" target="_self" tabindex="-1">
        <h4>ENVS: Environmental Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Finance/browse?sa=25ce03204f0f5b00eeb3eb4f0310c7b2" target="_self" tabindex="-1">
        <h4>FINS: Finance</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/FoodTechnology/browse?sa=61ce03204f0f5b00eeb3eb4f0310c7b7" target="_self" tabindex="-1">
        <h4>FOOD: Food Technology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/BusinessTechnology/browse?sa=3b5f5e79dbf393000595c4048a961929" target="_self" tabindex="-1">
        <h4>GBAT: Business Technology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/UnswBusinessSchool/browse?sa=adce03204f0f5b00eeb3eb4f0310c7bb" target="_self" tabindex="-1">
        <h4>GENC: UNSW Business School</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GeneralEducationFacultyOfEngineering/browse?sa=e9ce03204f0f5b00eeb3eb4f0310c7c0" target="_self" tabindex="-1">
        <h4>GENE: General Education - Faculty of Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GeneralEducationFacultyOfLaw/browse?sa=29ce03204f0f5b00eeb3eb4f0310c7c5" target="_self" tabindex="-1">
        <h4>GENL: General Education - Faculty of Law</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GeneralEducationFacultyOfMedicine/browse?sa=65ce03204f0f5b00eeb3eb4f0310c7ca" target="_self" tabindex="-1">
        <h4>GENM: General Education - Faculty of Medicine</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GeneralEducationFacultyOfScience/browse?sa=a1ce03204f0f5b00eeb3eb4f0310c7cf" target="_self" tabindex="-1">
        <h4>GENS: General Education - Faculty of Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/GeneralEducationTheLearningCentre/browse?sa=fdce03204f0f5b00eeb3eb4f0310c7d3" target="_self" tabindex="-1">
        <h4>GENY: General Education - The Learning Centre</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Geology/browse?sa=775f5e79dbf393000595c4048a96192e" target="_self" tabindex="-1">
        <h4>GEOL: Geology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Geoscience/browse?sa=3dce03204f0f5b00eeb3eb4f0310c7d8" target="_self" tabindex="-1">
        <h4>GEOS: Geoscience</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SurveyingSpatialInformationSystems/browse?sa=79ce03204f0f5b00eeb3eb4f0310c7dd" target="_self" tabindex="-1">
        <h4>GMAT: Surveying & Spatial Information Systems</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Architecture/browse?sa=2618bde7dbbce7040595c4048a9619c1" target="_self" tabindex="-1">
        <h4>GSBE: Architecture</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Engineering/browse?sa=b5ce03204f0f5b00eeb3eb4f0310c7e2" target="_self" tabindex="-1">
        <h4>GSOE: Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/HealthDataScience/browse?sa=b35f5e79dbf393000595c4048a961933" target="_self" tabindex="-1">
        <h4>HDAT: Health Data Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/HealthAndExerciseScience/browse?sa=f1ce03204f0f5b00eeb3eb4f0310c7e7" target="_self" tabindex="-1">
        <h4>HESC: Health and Exercise Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/HumanitiesAndLanguages/browse?sa=02287de7dbbce7040595c4048a961942" target="_self" tabindex="-1">
        <h4>HUML: Humanities and Languages</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Humanities/browse?sa=31ce03204f0f5b00eeb3eb4f0310c7ec" target="_self" tabindex="-1">
        <h4>HUMS: Humanities</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/IndustrialDesign/browse?sa=7dce03204f0f5b00eeb3eb4f0310c7f0" target="_self" tabindex="-1">
        <h4>IDES: Industrial Design</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/InstituteOfEnvironmentalStudies/browse?sa=ff5f5e79dbf393000595c4048a961937" target="_self" tabindex="-1">
        <h4>IEST: Institute of Environmental Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/IndustrialChemistry/browse?sa=b9ce03204f0f5b00eeb3eb4f0310c7f5" target="_self" tabindex="-1">
        <h4>INDC: Industrial Chemistry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/InformationSystems/browse?sa=f5ce03204f0f5b00eeb3eb4f0310c7fa" target="_self" tabindex="-1">
        <h4>INFS: Information Systems</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Innovation/browse?sa=35ce03204f0f5b00eeb3eb4f0310c7ff" target="_self" tabindex="-1">
        <h4>INOV: Innovation</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/InternationalStudies/browse?sa=71ce43204f0f5b00eeb3eb4f0310c704" target="_self" tabindex="-1">
        <h4>INST: International Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/InteriorArchitecture/browse?sa=bdce43204f0f5b00eeb3eb4f0310c708" target="_self" tabindex="-1">
        <h4>INTA: Interior Architecture</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Japanese/browse?sa=3f5f5e79dbf393000595c4048a96193c" target="_self" tabindex="-1">
        <h4>JAPN: Japanese</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/JurisDoctor/browse?sa=7b5f5e79dbf393000595c4048a961941" target="_self" tabindex="-1">
        <h4>JURD: Juris Doctor</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/KoreanStudies/browse?sa=b75f5e79dbf393000595c4048a961946" target="_self" tabindex="-1">
        <h4>KORE: Korean Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/LandscapeArchitecture/browse?sa=f9ce43204f0f5b00eeb3eb4f0310c70d" target="_self" tabindex="-1">
        <h4>LAND: Landscape Architecture</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Law/browse?sa=39ce43204f0f5b00eeb3eb4f0310c712" target="_self" tabindex="-1">
        <h4>LAWS: Law</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Linguistics/browse?sa=f35f5e79dbf393000595c4048a96194b" target="_self" tabindex="-1">
        <h4>LING: Linguistics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ManufacturingEngineering/browse?sa=75ce43204f0f5b00eeb3eb4f0310c717" target="_self" tabindex="-1">
        <h4>MANF: Manufacturing Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Marketing/browse?sa=b1ce43204f0f5b00eeb3eb4f0310c71c" target="_self" tabindex="-1">
        <h4>MARK: Marketing</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Mathematics/browse?sa=cece43204f0f5b00eeb3eb4f0310c720" target="_self" tabindex="-1">
        <h4>MATH: Mathematics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MaterialsScienceAndEngineering/browse?sa=0ece43204f0f5b00eeb3eb4f0310c725" target="_self" tabindex="-1">
        <h4>MATS: Materials Science and Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Management/browse?sa=335f5e79dbf393000595c4048a961950" target="_self" tabindex="-1">
        <h4>MBAX: Management</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Medicine/browse?sa=3738712bdbbce7040595c4048a96193e" target="_self" tabindex="-1">
        <h4>MDCN: Medicine</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Media/browse?sa=4ace43204f0f5b00eeb3eb4f0310c72a" target="_self" tabindex="-1">
        <h4>MDIA: Media</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MechanicalEngineering/browse?sa=86ce43204f0f5b00eeb3eb4f0310c72f" target="_self" tabindex="-1">
        <h4>MECH: Mechanical Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Medicine/browse?sa=c2ce43204f0f5b00eeb3eb4f0310c734" target="_self" tabindex="-1">
        <h4>MFAC: Medicine</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Finance/browse?sa=7f5f5e79dbf393000595c4048a961954" target="_self" tabindex="-1">
        <h4>MFIN: Finance</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Management/browse?sa=02ce43204f0f5b00eeb3eb4f0310c739" target="_self" tabindex="-1">
        <h4>MGMT: Management</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Microbiology/browse?sa=4ece43204f0f5b00eeb3eb4f0310c73d" target="_self" tabindex="-1">
        <h4>MICR: Microbiology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MiningEngineering/browse?sa=8ace43204f0f5b00eeb3eb4f0310c742" target="_self" tabindex="-1">
        <h4>MINE: Mining Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MechanicalManufacturingEngineering/browse?sa=c6ce43204f0f5b00eeb3eb4f0310c747" target="_self" tabindex="-1">
        <h4>MMAN: Mechanical & Manufacturing Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Management/browse?sa=bb5f5e79dbf393000595c4048a961959" target="_self" tabindex="-1">
        <h4>MNGT: Management</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Mining/browse?sa=f75f5e79dbf393000595c4048a96195e" target="_self" tabindex="-1">
        <h4>MNNG: Mining</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ModernLanguageStudies/browse?sa=375f5e79dbf393000595c4048a961963" target="_self" tabindex="-1">
        <h4>MODL: Modern Language Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MarineScience/browse?sa=06ce43204f0f5b00eeb3eb4f0310c74c" target="_self" tabindex="-1">
        <h4>MSCI: Marine Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MechatronicEngineering/browse?sa=0ace43204f0f5b00eeb3eb4f0310c75d" target="_self" tabindex="-1">
        <h4>MTRN: Mechatronic Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/UrbanPolicyAndStrategy/browse?sa=735f5e79dbf393000595c4048a961968" target="_self" tabindex="-1">
        <h4>MUPS: Urban Policy and Strategy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Music/browse?sa=46ce43204f0f5b00eeb3eb4f0310c762" target="_self" tabindex="-1">
        <h4>MUSC: Music</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Nanotechnology/browse?sa=82ce43204f0f5b00eeb3eb4f0310c767" target="_self" tabindex="-1">
        <h4>NANO: Nanotechnology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/NavalArchitecture/browse?sa=cece43204f0f5b00eeb3eb4f0310c76b" target="_self" tabindex="-1">
        <h4>NAVL: Naval Architecture</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/HivSocialResearch/browse?sa=6b487de7dbbce7040595c4048a961948" target="_self" tabindex="-1">
        <h4>NCHR: HIV Social Research</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Neuroscience/browse?sa=0ece43204f0f5b00eeb3eb4f0310c770" target="_self" tabindex="-1">
        <h4>NEUR: Neuroscience</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Optometry/browse?sa=4ace43204f0f5b00eeb3eb4f0310c775" target="_self" tabindex="-1">
        <h4>OPTM: Optometry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Pathology/browse?sa=86ce43204f0f5b00eeb3eb4f0310c77a" target="_self" tabindex="-1">
        <h4>PATH: Pathology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Pharmacology/browse?sa=c2ce43204f0f5b00eeb3eb4f0310c77f" target="_self" tabindex="-1">
        <h4>PHAR: Pharmacology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PublicHealthAndCommunityMedicine/browse?sa=12ce43204f0f5b00eeb3eb4f0310c784" target="_self" tabindex="-1">
        <h4>PHCM: Public Health and Community Medicine</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PublicHealthOffshoreProgram/browse?sa=bf5f5e79dbf393000595c4048a96196c" target="_self" tabindex="-1">
        <h4>PHOP: Public Health Offshore Program</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Physiology/browse?sa=5ece43204f0f5b00eeb3eb4f0310c788" target="_self" tabindex="-1">
        <h4>PHSL: Physiology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Photonics/browse?sa=9ace43204f0f5b00eeb3eb4f0310c78d" target="_self" tabindex="-1">
        <h4>PHTN: Photonics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Physics/browse?sa=d6ce43204f0f5b00eeb3eb4f0310c792" target="_self" tabindex="-1">
        <h4>PHYS: Physics</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PlanningAndUrbanDevelopment/browse?sa=16ce43204f0f5b00eeb3eb4f0310c797" target="_self" tabindex="-1">
        <h4>PLAN: Planning and Urban Development</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PoliticalScience/browse?sa=fb5f5e79dbf393000595c4048a961971" target="_self" tabindex="-1">
        <h4>POLS: Political Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PolymerScience/browse?sa=52ce43204f0f5b00eeb3eb4f0310c79c" target="_self" tabindex="-1">
        <h4>POLY: Polymer Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Psychiatry/browse?sa=3b5f5e79dbf393000595c4048a961976" target="_self" tabindex="-1">
        <h4>PSCY: Psychiatry</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Psychology/browse?sa=9ece43204f0f5b00eeb3eb4f0310c7a0" target="_self" tabindex="-1">
        <h4>PSYC: Psychology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PetroleumEngineering/browse?sa=dace43204f0f5b00eeb3eb4f0310c7a5" target="_self" tabindex="-1">
        <h4>PTRL: Petroleum Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/RegistrarsDivision/browse?sa=1ace43204f0f5b00eeb3eb4f0310c7aa" target="_self" tabindex="-1">
        <h4>REGZ: Registrar's Division</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/RealEstate/browse?sa=775f5e79dbf393000595c4048a96197b" target="_self" tabindex="-1">
        <h4>REST: Real Estate</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/RiskManagement/browse?sa=56ce43204f0f5b00eeb3eb4f0310c7af" target="_self" tabindex="-1">
        <h4>RISK: Risk Management</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SafetyScience/browse?sa=b35f5e79dbf393000595c4048a961980" target="_self" tabindex="-1">
        <h4>SAFE: Safety Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ArtHistory/browse?sa=92ce43204f0f5b00eeb3eb4f0310c7b4" target="_self" tabindex="-1">
        <h4>SAHT: Art History</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Art/browse?sa=dece43204f0f5b00eeb3eb4f0310c7b8" target="_self" tabindex="-1">
        <h4>SART: Art</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/FacultyOfScience/browse?sa=1ece43204f0f5b00eeb3eb4f0310c7bd" target="_self" tabindex="-1">
        <h4>SCIF: Faculty of Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/DesignStudies/browse?sa=5ace43204f0f5b00eeb3eb4f0310c7c2" target="_self" tabindex="-1">
        <h4>SDES: Design Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SoftwareEngineering/browse?sa=96ce43204f0f5b00eeb3eb4f0310c7c7" target="_self" tabindex="-1">
        <h4>SENG: Software Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ServicesMarketingTourismAndHospitality/browse?sa=d2ce43204f0f5b00eeb3eb4f0310c7cc" target="_self" tabindex="-1">
        <h4>SERV: Services Marketing - Tourism and Hospitality</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SafetyScience/browse?sa=3b587967dbbce7040595c4048a961919" target="_self" tabindex="-1">
        <h4>SESC: Safety Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialScienceAndPolicy/browse?sa=df68b52bdbbce7040595c4048a9619dd" target="_self" tabindex="-1">
        <h4>SLSP: Social Science and Policy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialWork/browse?sa=ff5f5e79dbf393000595c4048a961984" target="_self" tabindex="-1">
        <h4>SOCF: Social Work</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialWork/browse?sa=22ce43204f0f5b00eeb3eb4f0310c7d1" target="_self" tabindex="-1">
        <h4>SOCW: Social Work</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PhotovoltaicsAndSolarEnergy/browse?sa=6ece43204f0f5b00eeb3eb4f0310c7d5" target="_self" tabindex="-1">
        <h4>SOLA: Photovoltaics and Solar Energy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MediaArts/browse?sa=aace43204f0f5b00eeb3eb4f0310c7da" target="_self" tabindex="-1">
        <h4>SOMA: Media Arts</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/MedicalScience/browse?sa=e6ce43204f0f5b00eeb3eb4f0310c7df" target="_self" tabindex="-1">
        <h4>SOMS: Medical Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialSciences/browse?sa=4f78f12bdbbce7040595c4048a9619cc" target="_self" tabindex="-1">
        <h4>SOSS: Social Sciences</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialPolicy/browse?sa=b78875e7dbbce7040595c4048a96197d" target="_self" tabindex="-1">
        <h4>SPRC: Social Policy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SocialResearchAndPolicy/browse?sa=26ce43204f0f5b00eeb3eb4f0310c7e4" target="_self" tabindex="-1">
        <h4>SRAP: Social Research and Policy</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ArtsAndMedia/browse?sa=f798712bdbbce7040595c4048a961982" target="_self" tabindex="-1">
        <h4>STAM: Arts and Media</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/StrategyAndEntrepreneurship/browse?sa=a7a8b52bdbbce7040595c4048a9619cb" target="_self" tabindex="-1">
        <h4>STRE: Strategy and Entrepreneurship</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/SustainableDevelopment/browse?sa=3f5f5e79dbf393000595c4048a961989" target="_self" tabindex="-1">
        <h4>SUSD: Sustainable Development</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/WomenChildrensHealth/browse?sa=7b5f5e79dbf393000595c4048a96198e" target="_self" tabindex="-1">
        <h4>SWCH: Women & Children's Health</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/TaxationAndBusinessLaw/browse?sa=62ce43204f0f5b00eeb3eb4f0310c7e9" target="_self" tabindex="-1">
        <h4>TABL: Taxation and Business Law</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Telecommunications/browse?sa=a2ce43204f0f5b00eeb3eb4f0310c7ee" target="_self" tabindex="-1">
        <h4>TELE: Telecommunications</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/UrbanDevelopmentStudies/browse?sa=b75f5e79dbf393000595c4048a961993" target="_self" tabindex="-1">
        <h4>UDES: Urban Development Studies</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/VisionScience/browse?sa=eace43204f0f5b00eeb3eb4f0310c7f6" target="_self" tabindex="-1">
        <h4>VISN: Vision Science</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/EngineeringInformationTechnology/browse?sa=f35f5e79dbf393000595c4048a961998" target="_self" tabindex="-1">
        <h4>YCAN: Engineering & Information Technology</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/ArizonaStateUniversityMedicine/browse?sa=2ace43204f0f5b00eeb3eb4f0310c7fb" target="_self" tabindex="-1">
        <h4>YMED: Arizona State University Medicine</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/Business/browse?sa=66ce83204f0f5b00eeb3eb4f0310c700" target="_self" tabindex="-1">
        <h4>ZBUS: Business</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/InformationTechnologyElectricalEngineering/browse?sa=a2ce83204f0f5b00eeb3eb4f0310c705" target="_self" tabindex="-1">
        <h4>ZEIT: Information Technology & Electrical Engineering</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/UniversityCollegeGeneralEducation/browse?sa=a6ce83204f0f5b00eeb3eb4f0310c716" target="_self" tabindex="-1">
        <h4>ZGEN: University College General Education</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/HumanitiesSocialSciences/browse?sa=e2ce83204f0f5b00eeb3eb4f0310c71b" target="_self" tabindex="-1">
        <h4>ZHSS: Humanities & Social Sciences</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/UniversityCollegeinterdisciplinary/browse?sa=22ce83204f0f5b00eeb3eb4f0310c720" target="_self" tabindex="-1">
        <h4>ZINT: University College (Interdisciplinary)</h4>
      </a>
    </div>
      <div class="a-sauce">
      <a class="a-lettuce level-two" href="/PhysicalEnvironmentalMathematicalSciences/browse?sa=6ece83204f0f5b00eeb3eb4f0310c724" target="_self" tabindex="-1">
        <h4>ZPEM: Physical, Environmental & Mathematical Sciences</h4>
      </a>
    </div>
                                         </div>
          </div>
        </div>

              
      <hr class="a-onion" tabindex="-1">

            <hr class="a-onion" tabindex="-1">
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="http://timetable.unsw.edu.au" target="_blank" tabindex="-1">
          Class Timetable
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="https://student.unsw.edu.au/new-calendar" target="_blank" tabindex="-1">
          UNSW 3+
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="https://research.unsw.edu.au/" target="_blank" tabindex="-1">
          Research
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="https://www.futurestudents.unsw.edu.au/" target="_blank" tabindex="-1">
          Future Student
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="https://student.unsw.edu.au/" target="_blank" tabindex="-1">
          Current Student
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="https://my.unsw.edu.au/" target="_blank" tabindex="-1">
          My UNSW
        </a>
      </div>
            <div class="a-sauce">
        <a class="a-lettuce level-one" href="http://www.handbook.unsw.edu.au/general/2018/SSAPO/previousEditions.html" target="_blank" tabindex="-1">
          Pre-2019 Handbook
        </a>
      </div>
          </div>
  </div>
</div>              




<nav class="breadcrumbs" id="breadcrumbs-nav" role="navigation" aria-label="Breadcrumbs Navigation">
  <div class="a-wrapper">
  <ul>
    <li><a href="/">Home</a></li>
              
      
      
      
      
      
      
          
    
          <li aria-hidden="true"><span aria-hidden="true">/</span></li>
      <li class="crumb truncate"><span title="COMP1511 - Programming Fundamentals" tabindex="0">COMP1511 - Programming Fundamentals</span></li>
    
    </ul>
  </div>

                                                                                                                              </nav>

<script type="text/javascript">
 document.addEventListener('DOMContentLoaded', function() {
   // connect to redux store, get parameters, inject html into wrapper;
   const backButtonList = document.querySelectorAll('[data-hbui="take_me_back"]') ? document.querySelectorAll('[data-hbui="take_me_back"]') : [];
   if(backButtonList.length > 0) {
     [].forEach.call(backButtonList, function(backButton) {
       backButton.addEventListener('click', function(e) {
         e.preventDefault();
         console.log('***',window.history);
         if(window.history.length === 1) {
           window.location.href = '/';
         }

         window.history.back();

       })
     });
   }
 });
</script>
        
                        <header class="o-ai-overview" aria-label="Academic Item Header" style="border-top: 0">
  <div class="a-wrapper o-ai-overview-inner">
    <div class="o-ai-overview-inner-top">
              <div class="a-chip-row a-chip-row--overview">
                    <div tabIndex="0" class="a-chip">Course</div>
            <button data-hbui="a-btn-bookmark" class="a-btn-bookmark">
    <span
      class="a-icon a-btn-bookmark-icon"
      aria-label="Enter to save Program to your shortlist">
      bookmark_border
    </span>
    <span
      class="a-icon a-btn-bookmark-icon--selected"
      aria-label="You have saved Program to your shortlist. Enter to remove from your shortlist">
      bookmark
    </span>
  </button>
        </div>
      
      <h1 class="o-ai-overview__h1"><span data-hbui="module-title">Programming Fundamentals</span></h1>
    </div>

    <div class="m-ai-overview-details">
      <div class="m-ai-overview-details__cell code p-left-0"><strong>COMP1511</strong></div>

      <div class="m-ai-overview-details__cell code" data-credit-points>
                  <span class="hide-xs"><strong>6 Units of Credit</strong></span>
          <span class="hide-lg hide-md hide-sm"><strong>6 UOC</strong></span>
              </div>

      <div  class="m-ai-overview-details__cell" style="justify-content: flex-end">
        <div id="year_switcher"></div>
        <span
          data-hbui-helptext-static
          data-hbui-type="tooltip"
          data-hbui-tooltip-for="Year switcher"
          data-hbui-tooltip-text-content="Select the relevant year of handbook information you wish to view."
          style="margin-top: -0.3rem;"
        ></span>  
      </div> 
    </div>
  </div>
</header>

<script>
  document.addEventListener('DOMContentLoaded', function(e) {
    var endpoint = window.location.href.replace("/2020", "/${year}")
    var validYears = [{"label":"2019","value":"2019"},{"label":"2020","value":"2020"}] || [];
    ReactDOM.render(
      React.createElement(handbook.YearSwitcherReact,
        {
          callback: 'rescript',
          yearCookie: "implementation_year",
          year: "2020",
          endpoint: endpoint,
          interpolate: true,
          ES_HOST: '',
          code: "COMP1511",
          contentType: "subject",
          validYears: [{"label":"2019","value":"2019"},{"label":"2020","value":"2020"}],
          olderVersionMsg: "There is a newer version of this academic item available"
        }),
      document.querySelector('#year_switcher')
    ); 
  });
</script>
                <div class="a-wrapper">
                                    <div id="year_switcher_alert" role="alert" aria-live="assertive"></div>
                            
        
        
                                
                                            	            	                <div class="a-row">
	            	                	                
	                    	                    	                     	                    	                        	                    	                    	                        	                    	                        	                    	                        	                    	                        	                    
	                    <div class="a-column a-column-df-12">
	                        	                            






                        
  
    <div class="a-row m-top-1 ai-main-content" data-content>
    <div class="a-column a-column-df-2 a-column-lg-12 a-sticky m-page-nav-sticky no-print" id="pageNavContainer" aria-labelledby="menuDescription" data-hbui="sticky" role="navigation">
      <!-- Nav will be moved here after page load with JS -->
    </div>
    <!-- WCAG role="main" -->
    <div role="main" aria-label="Main Content" class="a-column a-column-df-7 a-column-lg-9 a-column-md-12">
      <span class="sr-only" id="menuDescription">Academic Item Menu</span>
      <div class="a-card m-bottom-2" id="subject-intro">
      <h3 tabindex="0" data-hbui="readmore__heading"><span data-hbui="module-title">Overview</span></h3>
<div data-hbui="readmore" tabindex="0" id="readMoreToggle1" class="m-read-more-toggle">
  <div data-hbui="readmore__toggle-text" class="a-card-text m-toggle-text ">
    <div class="readmore__wrapper">
              
<p>An introduction to problem-solving via programming, which aims to have students develop proficiency in using a high level programming language. Topics: algorithms, program structures (statements, sequence, selection, iteration, functions), data types (numeric, character), data structures (arrays, tuples, pointers, lists), storage structures (memory, addresses), introduction to analysis of algorithms, testing, code quality, teamwork, and reflective practice. The course includes extensive practical work in labs and programming projects.</p>
<p>Additional Information</p>
<p>This course should be taken by all CSE majors, and any other students who have an interest in computing or who wish to be extended. It does not require any prior computing knowledge or experience.</p>
<p>COMP1511 leads on to COMP1521, COMP1531, COMP2511 and COMP2521, which form the core of the study of computing at UNSW and which are pre-requisites for the full range of further computing courses.</p>
<p>Due to overlapping material, students who complete COMP1511 may not also enrol in COMP1911 or COMP1921. </p>
                                  </div>
  </div>
  <div class="a-card-footer m-read-more-footer">
    <a tabIndex="0" data-hbui="readmore__toggler" role="button" tabindex="-1" aria-hidden="true" class="m-read-more" href="#">
      Read More <span>COMP1511 Programming Fundamentals</span>
    </a>
    <a tabindex="0" data-hbui="readmore__toggler" role="button" tabindex="-1" aria-hidden="true" class="m-show-less" href="#">
      Read Less <span>COMP1511 Programming Fundamentals</span>
    </a>
  </div>
</div>
  </div>
      <div class="hide-md hide-lg">
        











<div class="a-card a-card-blue m-bottom-2 p-top-0">
  <div class="a-row a-row-equal-height o-attributes-table">

          <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Faculty</strong>
                      <a href="https://www.engineering.unsw.edu.au" target="_blank">Faculty of Engineering</a>
                </div>
    </div>
            <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">School</strong>
                      <a href="http://www.cse.unsw.edu.au/" target="_blank">School of Computer Science and Engineering</a>
                </div>
    </div>
            <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Study Level</strong>
                                  <p tabindex="0" class="enable-helptext">Undergraduate</p>
                </div>
    </div>
                    <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Offering Terms</strong>
                                  <p tabindex="0" class="">Term 1, Term 2, Term 3</p>
                </div>
    </div>
  
                                  <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Campus</strong>
                      <p tabindex="0">
                                                Kensington                                          </p>
      </div>
    </div>
                  <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Indicative contact hours</strong>
                                  <p tabindex="0" class="">7</p>
                </div>
    </div>
  
                <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item no-border">
        <strong tabindex="0">Timetable</strong>
                                  <a href="http://timetable.unsw.edu.au/2020/COMP1511.html" target="_blank">Visit timetable website for details</a>
                </div>
    </div>
        </div>
</div>      </div>
      

  
      


                                
            
        <div class="a-card a-card--has-body" id="equivalence-rules">
        <div class="a-card-body">
                  <h3 tabindex="0" >Equivalent Courses</h3>
                      <div data-hbui="course-list" class="o-course-list">
                <div class="m-single-course-wrapper">
    <a href="/undergraduate/courses/2020/DPST1091/

" target="_blank" class="m-single-course with-icon muted  ">
      <span class="a-icon" aria-hidden="true">arrow_forward</span>
      <div class="m-single-course-top-row">
        <span class="align-left">DPST1091</span>
                  <span>6 UOC</span>
              </div>
      <div class="m-single-course-bottom-row">
        <p class="text-color-blue-400 no-margin">Introduction to Programming</p>
      </div>
    </a>
  </div>
                <div class="m-single-course-wrapper">
    <a href="/undergraduate/courses/2020/COMP1917/

" target="_blank" class="m-single-course with-icon muted pointer-events-none a-link-disabled ">
      <span class="a-icon" aria-hidden="true">arrow_forward</span>
      <div class="m-single-course-top-row">
        <span class="align-left">COMP1917</span>
                  <span>6 UOC</span>
              </div>
      <div class="m-single-course-bottom-row">
        <p class="text-color-blue-400 no-margin">Computing 1</p>
      </div>
    </a>
  </div>
      </div>

            </div>
    </div>
      


                  
            
        <div class="a-card a-card--has-body" id="exclusion-rules">
        <div class="a-card-body">
                  <h3 tabindex="0" >Exclusion Courses</h3>
                      <div data-hbui="course-list" class="o-course-list">
                <div class="m-single-course-wrapper">
    <a href="/undergraduate/courses/2020/DPST1091/

" target="_blank" class="m-single-course with-icon muted  ">
      <span class="a-icon" aria-hidden="true">arrow_forward</span>
      <div class="m-single-course-top-row">
        <span class="align-left">DPST1091</span>
                  <span>6 UOC</span>
              </div>
      <div class="m-single-course-bottom-row">
        <p class="text-color-blue-400 no-margin">Introduction to Programming</p>
      </div>
    </a>
  </div>
      </div>

            </div>
    </div>

      

    <div class="a-card m-bottom-2" id="subject-outline">
    <h3  tabindex="0">Course Outline</h3>
          <p class="with-border" tabIndex="0">To access course outline, please visit:</p>
        <div class="m-button-group m-button-group--list">
              <a tabIndex="0" class="a-btn-secondary a-btn-secondary--with-icon" href="http://www.cse.unsw.edu.au/~cs1511/" target="_blank" aria-label="COMP1511 Course Outline">
          COMP1511 Course Outline
          <span aria-hidden="true" class="a-icon">open_in_new</span>
        </a>
          </div>
  </div>
      


                    


  <div class="a-card m-bottom-2" id="subject-fees">
    <h3  tabindex="0">Fees</h3>
    <div class="a-wrapper a-table m-bottom-1" role="table" aria-label="Fees table">
      <div class="a-row a-table-header" role="rowgroup">
        <div role="row" style="flex: 1 0 100%; display: flex;">
          <div class="a-column a-column-df-8" role="columnheader">
                          <small class="muted">Type</small>
                      </div>
          <div class="a-column a-column-df-4"  role="columnheader">
                          <small class="muted">Amount</small>
                      </div>
        </div>
      </div>
      <div role="rowgroup">
              <div class="a-row" role="row">
      <div class="a-column a-column-df-8 a-column-sm-12" role="cell">
        <a href='https://student.unsw.edu.au/fees-student-contribution-rates' target="_blank" aria-label='Commonwealth Supported Students'>
          <span aria-hidden="true" class="a-icon">open_in_new</span>
          Commonwealth Supported Students
        </a>
      </div>
      <div class="a-column a-column-df-4 a-column-sm-12" role="cell">
        <p tabindex="0" class="muted no-margin">
                      $1191
                  </p>
      </div>
    </div>
                <div class="a-row" role="row">
      <div class="a-column a-column-df-8 a-column-sm-12" role="cell">
        <a href='https://student.unsw.edu.au/fees-domestic-full-fee-paying' target="_blank" aria-label='Domestic Students'>
          <span aria-hidden="true" class="a-icon">open_in_new</span>
          Domestic Students
        </a>
      </div>
      <div class="a-column a-column-df-4 a-column-sm-12" role="cell">
        <p tabindex="0" class="muted no-margin">
                      $5970
                  </p>
      </div>
    </div>
                <div class="a-row" role="row">
      <div class="a-column a-column-df-8 a-column-sm-12" role="cell">
        <a href='https://student.unsw.edu.au/fees-international' target="_blank" aria-label='International Students'>
          <span aria-hidden="true" class="a-icon">open_in_new</span>
          International Students
        </a>
      </div>
      <div class="a-column a-column-df-4 a-column-sm-12" role="cell">
        <p tabindex="0" class="muted no-margin">
                      $5970
                  </p>
      </div>
    </div>
        </div>
    </div>
                                    <div class="a-card-footer a-card-footer-reverse">
      <strong tabindex="0">DISCLAIMER</strong>
      <p class="no-margin" tabindex="0">
        Please note that the University reserves the right to vary student fees in line with relevant legislation. This fee information is provided as a guide and more specific information about fees, including fee policy, can be found on the <a href="https://student.unsw.edu.au/fees" target="_blank">fee website</a>. 
<br><br>For advice about fees for courses with a fee displayed as "Not Applicable", including some Work Experience and UNSW Canberra at ADFA courses, please contact the relevant Faculty. 
<br><br>Where a Commonwealth Supported Students fee is displayed, it does not guarantee such places are available. 
      </p>
    </div>
        </div>
       

                          

  <div class="a-card m-bottom-2" id="subject-additional">
    <h3  tabindex="0">Additional Information</h3>
    <div class="a-wrapper a-table">
                    <div class="a-row">
      <div class="a-column a-column-df-12 a-column-sm-12">
        <p class="no-margin" tabindex="0">This course is offered as General Education.</p>
      </div>
    </div>
            </div>
  </div>
      



  <div class="a-card a-card--has-body m-bottom-2 p-bottom-0 bgc-gray-200" id="previousHandbook">
    <div class="a-card-body">
      <h3 tabindex="0">
        Pre-2019 Handbook Editions
      </h3>
      <p tabindex="0">Access past handbook editions (2018 and prior)</p>
      <div class="m-button-group m-button-group--list m-bottom-1">
        <a tabIndex="0" class="a-btn-secondary a-btn-secondary--with-icon" href="http://www.handbook.unsw.edu.au/general/2018/SSAPO/previousEditions.html" target="_blank" aria-label="Previous Handbook">
          Pre-2019 Handbook Editions
          <span aria-hidden="true" class="a-icon">open_in_new</span>
        </a>
      </div>
    </div>
  </div>
            <div class="a-column hide-md hide-lg m-top-3 m-bottom-1">
        <div class="a-row" role="region" aria-labelledby="utilRegion">
          <span class="sr-only" id="utilRegion">Helpful utilities like sharing or printing this page</span>
          <div style="flex:1 0 100%" class="m-right-1">
            





      <div class="m-bottom-1">
  <span aria-hidden="true" class="a-icon m-right-1 m-left-1" aria-label="Click enter to send a copy of COMP1511 - Programming Fundamentals via email" style="opacity: .54">local_post_office</span>
  <a data-hbui="email_link" data-body="Hi! I found this page from UNSW that you might be interested in:" data-subject="UNSW link to Course: COMP1511 - Programming Fundamentals">Share Link via Email</a>
</div>
        
<div class="m-bottom-1">
  <span aria-hidden="true" class="a-icon m-right-1 m-left-1" style="opacity: .54">get_app</span>
  <a target="_blank" href="https://itq9q5ny14.execute-api.ap-southeast-2.amazonaws.com/prod/pdf?url=https://www.handbook.unsw.edu.au/undergraduate/courses/2020/comp1511/" data-hbui="pdf_link">Download PDF</a>
</div>
  
          </div>
        </div>
      </div>
    </div>

    <div class="a-column a-column-df-3 hide-xs hide-sm no-print">
      <div role="complementary" aria-label="Complementary Academic Item Information">
        











<div class="a-card a-card-blue m-bottom-2 p-top-0">
  <div class="a-row a-row-equal-height o-attributes-table">

          <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Faculty</strong>
                      <a href="https://www.engineering.unsw.edu.au" target="_blank">Faculty of Engineering</a>
                </div>
    </div>
            <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">School</strong>
                      <a href="http://www.cse.unsw.edu.au/" target="_blank">School of Computer Science and Engineering</a>
                </div>
    </div>
            <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Study Level</strong>
                                  <p tabindex="0" class="enable-helptext">Undergraduate</p>
                </div>
    </div>
                    <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Offering Terms</strong>
                                  <p tabindex="0" class="">Term 1, Term 2, Term 3</p>
                </div>
    </div>
  
                                  <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Campus</strong>
                      <p tabindex="0">
                                                Kensington                                          </p>
      </div>
    </div>
                  <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item ">
        <strong tabindex="0">Indicative contact hours</strong>
                                  <p tabindex="0" class="">7</p>
                </div>
    </div>
  
                <div class="a-column a-column-df-12 a-column-md-6 a-column-sm-12">
      <div class="o-attributes-table-item no-border">
        <strong tabindex="0">Timetable</strong>
                                  <a href="http://timetable.unsw.edu.au/2020/COMP1511.html" target="_blank">Visit timetable website for details</a>
                </div>
    </div>
        </div>
</div>      </div>
      <div role="region" aria-labelledby="utilRegion2">
        <span class="sr-only" id="utilRegion2">Helpful utilities like sharing or printing this page</span>
        <div class="a-row p-all-1">
          





      <div class="m-bottom-1">
  <span aria-hidden="true" class="a-icon m-right-1 m-left-1" aria-label="Click enter to send a copy of COMP1511 - Programming Fundamentals via email" style="opacity: .54">local_post_office</span>
  <a data-hbui="email_link" data-body="Hi! I found this page from UNSW that you might be interested in:" data-subject="UNSW link to Course: COMP1511 - Programming Fundamentals">Share Link via Email</a>
</div>
        
<div class="m-bottom-1">
  <span aria-hidden="true" class="a-icon m-right-1 m-left-1" style="opacity: .54">get_app</span>
  <a target="_blank" href="https://itq9q5ny14.execute-api.ap-southeast-2.amazonaws.com/prod/pdf?url=https://www.handbook.unsw.edu.au/undergraduate/courses/2020/comp1511/" data-hbui="pdf_link">Download PDF</a>
</div>
  
        </div>
      </div>

      <div>
                



<div class="a-quick-links a-card flat" style="padding: 0.1rem" role="navigation" aria-labelledby="linkDescriptionSideBar">
<span id="linkDescriptionSideBar" class="sr-only">Quick Links Section SideBar</span>

    
    <a href="https://student.unsw.edu.au/fees" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Fees Information</strong>
      <p style="margin-top:0.5rem">
                    Search UNSW fees and related policies
                        </p>
    </div>
  </a>
  
    
    <a href="https://student.unsw.edu.au/calendar	" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Academic Calendar</strong>
      <p style="margin-top:0.5rem">
                          Find out key dates in UNSW's Academic Calendar
                  </p>
    </div>
  </a>
  
    
    <a href="https://applyonline.unsw.edu.au/login
" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Apply Online</strong>
      <p style="margin-top:0.5rem">
                                Some programs require application via the Universities Admissions Centre (UAC) depending on study level, applicant's residency etc. Please check the "Can I apply online?" section on the Apply Online page to confirm whether to apply via the UNSW Apply Online service or through the UAC
            </p>
    </div>
  </a>
  </div>
      </div>
    </div>
    <div class="is-hidden no-print">

      <!-- WCAG role="nav" -->
      
  <div id="pageNav">
    <div class="m-page-nav m-bottom-2" data-hbui="mobile-nav">
      <span aria-label="Collapse page navigation" class="a-icon m-page-nav-icon m-page-nav-icon-collapse"><span aria-hidden="true">expand_more</span></span>
      <span aria-label="Expand page navigation" class="a-icon m-page-nav-icon m-page-nav-icon-expand"><span aria-hidden="true">expand_more</span></span>
      <button data-scroll-header class="m-page-nav-button"></button>
      <div data-gumshoe class="m-page-nav-list" role="list">
                  <div role="listitem">
            <a data-scroll href="#subject-intro" tabindex="0">Overview</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#equivalence-rules" tabindex="0">Equivalent Courses</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#exclusion-rules" tabindex="0">Exclusion Courses</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#subject-outline" tabindex="0">Course Outline</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#subject-fees" tabindex="0">Fees</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#subject-additional" tabindex="0">Additional Information</a>
          </div>
                  <div role="listitem">
            <a data-scroll href="#previousHandbook" tabindex="0">Pre-2019 Handbook Editions</a>
          </div>
              </div>
    </div>
  </div>
    </div>
  </div>
         
	                    </div><!--/span-->
	                	            </div><!--/row-->
                    
                                
	</div><!-- /container-->
  </div>
			




<!-- Start Before Footer dotParse -->
<!-- Responsive Quick Links SideBar (Footer) -->
<div class="hide-md hide-lg">
    



<div class="a-quick-links a-card flat" style="padding: 0.1rem" role="navigation" aria-labelledby="linkDescriptionFooter">
<span id="linkDescriptionFooter" class="sr-only">Quick Links Section Footer</span>

    
    <a href="https://student.unsw.edu.au/fees" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Fees Information</strong>
      <p style="margin-top:0.5rem">
                    Search UNSW fees and related policies
                        </p>
    </div>
  </a>
  
    
    <a href="https://student.unsw.edu.au/calendar	" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Academic Calendar</strong>
      <p style="margin-top:0.5rem">
                          Find out key dates in UNSW's Academic Calendar
                  </p>
    </div>
  </a>
  
    
    <a href="https://applyonline.unsw.edu.au/login
" class="a-card" target="_blank">
    <span class="a-icon" aria-hidden="true">open_in_new</span>
    <div>
      <strong>Apply Online</strong>
      <p style="margin-top:0.5rem">
                                Some programs require application via the Universities Admissions Centre (UAC) depending on study level, applicant's residency etc. Please check the "Can I apply online?" section on the Apply Online page to confirm whether to apply via the UNSW Apply Online service or through the UAC
            </p>
    </div>
  </a>
  </div>
</div>
<!-- Global Quick Links Footer -->





<div class="a-quick-links-footer three-col a-card flat" role="navigation" aria-labelledby="footerLinksDescription">
  <span class="sr-only" id="footerLinksDescription">Quick Links Section 2</span>
  <div class="footer-flex a-wrapper">
                    <a href="https://student.unsw.edu.au/elearning" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_1"><strong>eLearning</strong></span>
        <p>            Information on eLearning, IT support and apps for students
                                    </p>
      </div>
    </a>
                    <a href="https://unswinsight.microsoftcrmportals.com/handbook-questions/" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_2"><strong>Ask a question</strong></span>
        <p>                  All your UNSW Handbook questions answered here
                              </p>
      </div>
    </a>
                    <a href="https://www.unsw.edu.au/faculties" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_3"><strong>UNSW  Faculties</strong></span>
        <p>                        Visit Faculty websites for faculty-specific information
                        </p>
      </div>
    </a>
                    <a href="http://www.library.unsw.edu.au/" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_4"><strong>Library</strong></span>
        <p>                              Search the UNSW Library Catalogue
                  </p>
      </div>
    </a>
                    <a href="http://www.international.unsw.edu.au/" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_5"><strong>International Applicants</strong></span>
        <p>                                    Information for International students
            </p>
      </div>
    </a>
                    <a href="https://nucleus.unsw.edu.au/contactus" class="a-card m-bottom-1" target="_blank">
      <span class="a-icon" aria-hidden="true">open_in_new</span>
      <div>
        <span class="footer" id="footer_ql_6"><strong>The Nucleus: Student Hub</strong></span>
        <p>                                          Advice and support from enrolment through to graduation
      </p>
      </div>
    </a>
      </div>
</div>


  
  <div class="o-recently-viewed" data-hbui="recently-viewed" data-storage-element="CL-recently-viewed">
    <div class="a-wrapper">
      <header class="o-recently-viewed__header">
        <h3  tabindex="0" data-hbui="recently-viewed-heading">Recently viewed</h3>
              </header>
      <div class="m-fixed-width-grid-scroller" data-hbui="recently-viewed-content">
      </div>
    </div>
  </div>

  <script>
    var itemDetails = {
      org: 'CL',
      code: 'COMP1511',
      name: 'Programming Fundamentals',
      type: 'Course',
      year: '2020',
      maxItems: 4
    };
    document.addEventListener('DOMContentLoaded', function() {
      new handbook.RecentlyViewed(itemDetails);
      new handbook.ClearStorageHandler(document, localStorage);
    });
  </script>

  
    
  <div class="o-my-list " data-hbui="my-list">
    <div class="a-wrapper">
      <div class="o-my-list--header">
        <div class="o-my-list--icon">
          <div class="a-icon a-icon-small" aria-hidden="true">bookmark</div>
        </div>
        <h4  tabindex="0">My Lists</h4>
                                  <a href="/MyList" class="o-my-list--view-all">View all</a>
              </div>
      <div class="m-fixed-width-grid-scroller" data-hbui="my-list-content">
      </div>
    </div>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const MyList = new handbook.MyList({
        org: 'CL',
        maxItems: 4
      });
      new handbook.EditLocalStorage({
        key: `CL-bookmarks`,
        toggleEdit: MyList.toggleCanDelete,
        deleteAllItems: MyList.deleteAllItems,
        maxItems: 4
      }).init();
    });
  </script>
<!-- End Before Footer dotParse -->

 <footer class="o-footer" aria-label="Important information about this University">
	<div class="a-wrapper">
		<div class="a-row o-footer-top">
      <div class="a-column a-column-df-2 a-column-md-12 a-column-sm-12">
        <div class="o-footer-logo">
                                      </div>
      </div>
      <div class="a-column a-column-df-7 a-column-md-12 a-column-sm-12">
                  <p tabindex="0" class="with-double-margin">© UNSW Sydney (CRICOS Provider No.: 00098G), 2019. The information contained in this Handbook is indicative only. While every effort is made to keep this information up-to-date, the University reserves the right to discontinue or vary arrangements, programs and courses at any time without notice and at its discretion. While the University will try to avoid or minimise any inconvenience, changes may also be made to programs, courses and staff after enrolment. The University may also set limits on the number of students in a course.</p>
              </div>
      <div class="a-column a-column-df-3 a-column-md-12 a-column-sm-12 has-focus">
                  <p tabindex="0" id="footer_authorised">Authorised by Deputy Vice-Chancellor (Academic)</p>
                          <p tabindex="0" id="footer_cricos" class="no-margin">CRICOS Provider Code 00098G</p>
                          <p tabindex="0" id="footer_abn">ABN: 57 195 873 179</p>
              </div>
		</div>
	</div>
  <div class="o-footer-links">
    <div class="a-wrapper" role="navigation" aria-label="Links to important information such as copyright and privacy policy.">
      <div class="a-row">
        <div class="a-column a-column-df-10 a-column-md-12 a-column-sm-12 a-column-df-offset-2 a-column-md-offset-0">
                                  <a href="https://unsw.edu.au/copyright-disclaimer" target="_blank">Copyright and Disclaimer</a>
                                  <a href="https://unsw.edu.au/privacy" target="_blank">Privacy Policy</a>
                                  <a href="https://unsw.edu.au/accessibility" target="_blank">Accessibility</a>
                                              <a href="mailto:Handbook.editor@unsw.edu.au" target="_self">Site Feedback</a>
                  </div>
      </div>
    </div>
  </div>
</footer>

<!-- Start After Footer dotParse -->
<!-- Global Notifications -->
<div class="a-notification no-print" data-hbui="a-notification">
  <div class="a-notification--content" data-hbui="a-notification--bookmark">
    <div class="a-notification--message">
      <p>Saved into MyList</p>
    </div>
    <div class="a-notification--controls">
      <a href="/MyList">Go to MyList</a>
    </div>
  </div>
</div>

<!-- End After Footer dotParse -->

<!-- Place javascript in side of renderFooterJS -->
<script data-ys-ignore>
  document.addEventListener("DOMContentLoaded", function(event) {
    const org = 'CL';
    const bookmarksTitle = 'My Lists';

    window.handbookEvents = new handbook.EventEmitter();

    new handbook.SecondaryNav().init();
    new handbook.HamburgerHelper().init();

    if(window.location.pathname !== '/search') {
      document.querySelector('#a-nav-bookmark-link').focus();
    }

    handbook.Accessibility.run();
  })
</script>
<script type="application/javascript">
  document.addEventListener("DOMContentLoaded", function(event) {
    const org = 'CL';
    const bookmarksTitle = 'My Lists';

    new handbook.CreateBookmarksList({ org: org, bookmarksTitle: bookmarksTitle });
    new handbook.PageNav({ container: 'pageNavContainer'});

    const courseLists = document.querySelectorAll('[data-hbui="course-list"]');
    [].forEach.call(courseLists, function(el) {new handbook.CourseList({ container: el })});

            var academicItemLinks = document.querySelectorAll('[role="main"] a');
    var regExp = new RegExp("//" + location.host + "($|/)");
    [].forEach.call(academicItemLinks, function(el) {
      var href = el.getAttribute("href") || "";
      var target = el.getAttribute("target");
      var isLocal = (href.substring(0,4) === "http") ? regExp.test(href) : true;

      if (!isLocal && !target) {
        el.setAttribute("target", "_blank");
      }
    });


    var readMoreToggles = document.querySelectorAll('[data-hbui="readmore"]');
    [].forEach.call(readMoreToggles, function(el) {new handbook.ReadMoreAccordion({ container: el })});

    var accordions = [...document.querySelectorAll('[data-hbui="accordion"]')];
    handbook.renderedAccordions = accordions.map((accordion, index) => new handbook.Accordion({ container: accordion, accordionId: index }))

    var accordionLists = [...document.querySelectorAll('[data-hbui="accordion-list"]')];

    const renderedListAccordions = accordionLists.map(accordionList => new handbook.Accordion({ container: accordionList, list: true }));

        const hackCallback = (a => state => {
      const handleAccordions = (acc) => {
        if(state.expanded) acc.accordions.forEach((item) => { item.expand(); });
      }
      renderedListAccordions.forEach(handleAccordions);
    })(renderedListAccordions)

    new handbook.Hackordions([...document.querySelectorAll('[data-hackordion]')], hackCallback);

    var tabGroups = document.querySelectorAll('[data-hbui="tab-group"]');
    [].forEach.call(tabGroups, function(el) {new handbook.TabGroup({ container: el })});

    const filters = document.querySelectorAll('[data-hbui="filters"]');
    [].forEach.call(filters, function(el) {
      new handbook.Filters({ container: el });
    });

    handbook.initializeFilterGroups();
    const basicDropdowns = document.querySelectorAll('[data-hbui="dropdown-basic"]');
    [].forEach.call(basicDropdowns, function(el) { new handbook.DropDown({ container: el }) })

    var code = 'COMP1511';
    var name = 'Programming Fundamentals';
    var type = 'Course';
    var year = '2020';
    var notifications = new handbook.Notifications();

    setTimeout(function() {
        new handbook.Bookmarks({ code: code, notifications: notifications, org: org, type: type, year: year });
    }, 150);
    new handbook.TooltipJS().init();

    var printShare = new handbook.SharePrint();

    printShare.print();
    printShare.email();
    printShare.share();

    var helptext = window.config.getInstance('helptext');
    var helptextCopy1 = helptext.map(function(term) { return Object.assign({}, term)});
    var helptextCopy2 = helptext.map(function(term) { return Object.assign({}, term)});
    var helptextCopy3 = helptext.map(function(term) { return Object.assign({}, term)});

    var a = new handbook.HelpText({
        outerSelector: '[role="complementary"]',
        innerSelectors: ['.a-chip:not([data-hbui-filter])', '.o-attributes-table-item strong', '.enable-helptext'],
        terms: helptextCopy1,
    });

    var b = new handbook.HelpText({
        outerSelector: '[role="main"]',
        innerSelectors: ['.a-chip:not([data-hbui-filter])', '.m-accordion-group-footer h3', '.o-attributes-table-item strong', '.enable-helptext'],
        terms: helptextCopy2,
    });
        var c = new handbook.HelpText({
        outerSelector: '.o-ai-overview',
        innerSelectors: ['.a-chip:not([data-hbui-filter])', '.m-accordion-group-footer h3', '.o-attributes-table-item strong', '.enable-helptext'],
        terms: helptextCopy2,
    });
        var d = new handbook.HelpText(true).Tooltips.init();
    if (handbook.Sticky) {
        new handbook.Sticky({ offset: 50, offsetAt: 990, lift: '.o-course-list-separator-full:not([sticky-header])' });
    }
    
    var mobileNavs = document.querySelectorAll('[data-hbui="mobile-nav"]');
    [].forEach.call(mobileNavs, function(el) {new handbook.MobileNavigation({ container: el })});
  });
</script>
	
</body>
</html>
'''
