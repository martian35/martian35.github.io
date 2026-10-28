# Project page writing and figure guide

The public pages keep the existing compact academic layout. This file records the editorial decisions behind the October 2026 revision and how to update ongoing work.

## Give readers three levels of detail

1. **Homepage:** field, functional title, one-sentence purpose, result or status, and a verified role.
2. **Project overview:** problem, approach, outcome/status, and contribution; a representative image; a four-step explanation of the system; three or four concrete engineering decisions.
3. **Implementation notes:** the existing technical detail and source links, available in an expandable section.

Use the same structure to orient readers, but let the content explain each project's actual constraints. A model name is useful after a reader understands what goes in, what comes out, and why the connection matters.

## Make each image answer a question

| Project | Useful visual | What the reader should understand |
| --- | --- | --- |
| Gaussian mapping | Clearly labelled conceptual map and observation workflow | How poses, observations, representation, and evaluation relate; the illustration is not a measured result. |
| SplatAug-FR3 | Same episode from multiple cameras; scale-validation figure; episode montage | Reusable geometry must agree with metric dimensions, kinematics, and camera state. |
| Robot Challenge | Real prototype, arena layout, sensor-to-action workflow, links to final-run videos | The basket mechanism, observation timing, and delivery task constrain the software. |
| FastMRI | Team architecture and measurement-to-reconstruction workflow | Acquired data stays connected to the learned reconstruction. |
| Scene reordering | Conceptual ordering diagram and score-alignment workflow | The output is a permutation; evidence from different views must refer to the same frames. |
| Wind forecast | Original model architecture and evaluation slide | Physical baseline, residual correction, and ensemble have distinct roles. |
| Filming device | Real prototype, exploded assembly, visual-feedback workflow, demo links | Pixel error becomes actuator commands inside a complete device. |
| TaXer/WaXer | Team architecture, feature-fusion workflow, forecast traces | Features meet inside cross-attention rather than at the output of two forecasts. |

Figures stay next to the claims they explain. Full-size links preserve access to labels in original slides. Native HTML workflow figures reflow on small screens and remain readable as text. Photographs, architecture diagrams, conceptual illustrations, and measured results have different captions and should not be substituted for each other.

Do not synthesize benchmark plots, MRI examples, or robot trials from imagined data. When available, future additions should use matched baseline/method views and the same settings. A SLAM result should identify the scene, pose source, frame budget, baseline, and metric. A robot-learning result should identify the task, policy, real/synthetic data budget, number of trials, and success criterion.

## Connect the research without flattening the differences

The mapping project asks how a 3D representation is built and checked. The augmentation project asks how reconstructed assets can support robot-learning data. Earlier projects provide concrete examples of measurement consistency, physical constraints, representation interfaces, and software–hardware integration. These connections explain the research direction without claiming that all projects solve the same problem.

Both research entries remain ongoing. Manuscript preparation is not publication. Rendering and kinematic validation are not evidence of downstream physical policy success. Team-level implementation must stay distinct from individually verified contributions.

## Personal introduction

Keep the homepage introduction concise: academic background, broad research interests, and current laboratory work. Reflective paragraphs about engineering training, cultural background, and learning attitudes are excluded from the homepage. The manuscript is described only as a first-author manuscript in preparation, without a target venue.

Example SOPs and other people's CVs were used only as writing references. Their publications, roles, and achievements are not the user's credentials.

## Research and writing references

- User-supplied advice collection: [shaily99/advice](https://github.com/shaily99/advice), especially its links to the MIT EECS and Andy Pavlo guidance.
- [MIT EECS: Graduate School Statement of Purpose](https://mitcommlab.mit.edu/eecs/commkit/graduate-school-statement-of-purpose/): concrete contributions and the significance of experience; applied here to a website rather than copied as an application essay.
- [MIT EECS: Professional Bio](https://mitcommlab.mit.edu/eecs/commkit/professional-bio/): a clear professional identity supported by relevant experience.
- [MIT EECS: Figure Design](https://mitcommlab.mit.edu/eecs/commkit/figure-design/): one clear message per figure, matched to the audience and supported by appropriate evidence.
- [Andy Pavlo: How to Write a Bad Statement](https://www.cs.cmu.edu/~pavlo/blog/2015/10/how-to-write-a-bad-statement-for-a-computer-science-phd-admissions-application.html): avoid an irrelevant childhood-genius narrative.
- [Jon Barron](https://jonbarron.info/): retain the compact academic presentation and concise project summaries.
- [Seunghun Oh](https://alvin0808.github.io/): separate project context, technical contribution, result, and links.

Implementation evidence is linked on each project page and retained in `content/portfolio.json`. New image provenance is recorded in `content/image-sources.json`.

## Updating an ongoing entry

Edit `summary`, `at_glance`, `sections`, `technical_notes`, and `status` in `content/portfolio.json`. Keep completed implementations, observed measurements, and proposed experiments separate. Add the method/experimental conditions alongside any new result figure, then run the documented build and link checks.

## Scope corrections

The user clarified that their Robot Challenge contribution spans vision, planning, data collection, hardware, and integration. README role summaries must not narrow that first-hand account to vision alone. The Gaussian SLAM work has a first-author manuscript in preparation and no public repository. Do not name a planned submission venue. OpenMAVIS/Aria pipeline materials are not evidence for this manuscript and must not be linked as its implementation. The paper is in preparation, not submitted, under review, or accepted.
