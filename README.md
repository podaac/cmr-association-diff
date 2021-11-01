# cmr-association-diff

Python tool to compare tools and services collection associations in a text file to those in CMR. Results are collections in CMR and NOT in text file. Either concept id or provider and name is needed to run the command line tool.

## Usage

```
$ cmr_association_diff --help
usage: cmr_association_diff [-h] [-c] -e uat or ops [-p] [-n] -t
                            {tool,service} -a associations.txt
                            [-o OUTPUT_FILE]

Update CMR with latest profile

optional arguments:
  -h, --help            show this help message and exit
  -c , --concept_id     Concept id of umm to poll (default: None)
  -e uat or ops, --env uat or ops
                        CMR environment used to pull results from. (default:
                        None)
  -p , --provider       Provider of the umm (default: None)
  -n , --umm_name       Name of the umm tool or service (default: None)
  -t {tool,service}, --type {tool,service}
                        type of umm to poll (default: None)
  -a associations.txt, --assoc associations.txt
                        Association concept ID or file containing many concept
                        IDs to be associated with UMM provided. (default:
                        None)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File to output to (default: None)
```

## Example:

Tools

Using concept id
```
cmr_association_diff -c TL1240538128-POCLOUD -e uat -t tool -a hitide_uat_associations.txt
```

Using provider and name
```
cmr_association_diff -e uat -t tool -a hitide_uat_associations.txt -p POCLOUD -n hitide
```

Services

Using concept id
```
cmr_association_diff -c S1234899453 -e uat -t service -a hitide_uat_associations.txt
```

Using provider and name
```
cmr_association_diff -e uat -t service -a hitide_uat_associations.txt -p POCLOUD -n podaac_l2_cloud_subsetter
```